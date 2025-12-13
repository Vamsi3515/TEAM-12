"""
Experience Authenticity & Skill Consistency Agent

Analyzes consistency between resume claims and observable evidence (GitHub, LeetCode)
to generate confidence and risk signals about employability readiness.

This is a SUPPORTIVE, ETHICAL decision-support system - NOT a fraud detector.
"""

import json
import re
from typing import List, Dict, Any, Tuple, Optional
from app.core.llm_client import call_chat
from app.models.authenticity import (
    AuthenticityAnalysisInput,
    AuthenticityAnalysisOutput,
    AuthenticityExtendedInput,
    AuthenticityExtendedOutput,
    SkillAlignment,
    ResumeData,
    GitHubEvidence,
    LeetCodeEvidence,
    EvidenceItem,
    Claim,
    ClaimEvidenceMapping,
    ClaimVerification,
)


# ==================== PROMPT ENGINEERING ====================

def _create_authenticity_system_prompt() -> str:
    """System prompt for ethical, supportive skill consistency analysis."""
    return """You are an Experience Authenticity & Skill Consistency Agent - a supportive career coach that helps candidates understand the alignment between their resume claims and observable evidence.

CRITICAL PRINCIPLES:
- You are SUPPORTIVE and CANDIDATE-FRIENDLY, NOT accusatory
- You do NOT assume missing evidence means dishonesty
- You do NOT penalize candidates for not having GitHub or LeetCode
- Your job is to EXPLAIN evidence alignment, not make hiring decisions
- You highlight both strengths AND opportunities for improvement
- You are NEUTRAL and PROFESSIONAL in all assessments
- You NEVER use words like "fraud", "fake", "dishonest", "false", "deceptive"

TONE: Encouraging, constructive, non-judgmental, improvement-focused

Your analysis should:
1. Identify skills CLEARLY supported by evidence (GitHub repos, projects, commits, etc.)
2. Flag areas where evidence is WEAK or MISSING - without judgment
3. Suggest ACTIONABLE STEPS to strengthen evidence (e.g., "Consider adding a GitHub project that demonstrates X")
4. Recognize that not all skills require public proof (e.g., soft skills, internal company work)
5. Account for different career stages - early-career candidates may have limited GitHub presence

Output MUST be strict JSON only, no extra text."""


def _create_authenticity_analysis_prompt(
    resume: ResumeData,
    github: Optional[GitHubEvidence] = None,
    leetcode: Optional[LeetCodeEvidence] = None,
    additional_context: Optional[str] = None,
) -> str:
    """Create detailed analysis prompt with all candidate evidence."""
    
    prompt = f"""Analyze the following candidate's experience authenticity and skill consistency.

=== RESUME DATA ===
Skills Claimed: {", ".join(resume.skills) if resume.skills else "No skills listed"}
Experience Summary: {len(resume.experience)} roles mentioned
Projects: {len(resume.projects)} projects listed
Education: {len(resume.education)} education entries
Certifications: {", ".join(resume.certifications) if resume.certifications else "None"}

Resume Raw Text (if available):
{resume.raw_text if resume.raw_text else "Not provided"}

=== GITHUB EVIDENCE ===
"""
    
    if github:
        prompt += f"""Languages Used: {", ".join(github.languages) if github.languages else "Not analyzed"}
Repository Count: {github.repo_count}
Commit Frequency: {github.commit_frequency}
README Quality: {github.readme_quality}
Contribution Pattern: {github.contribution_pattern}
Top Projects: {len(github.top_projects)} analyzed

Top Project Details:
{json.dumps(github.top_projects, indent=2) if github.top_projects else "None"}

Profile Data: {json.dumps(github.raw_profile_data, indent=2) if github.raw_profile_data else "Not available"}
"""
    else:
        prompt += "GitHub data: NOT PROVIDED (This is okay - not all candidates have public GitHub)\n"
    
    prompt += "\n=== LEETCODE EVIDENCE ===\n"
    if leetcode and (leetcode.problems_solved > 0):
        prompt += f"""Problems Solved: {leetcode.problems_solved}
Difficulty Distribution: {json.dumps(leetcode.difficulty_distribution)}
Recent Activity: {"Yes" if leetcode.recent_activity else "No"}
Ranking: {leetcode.ranking or "Not available"}

Raw Data: {json.dumps(leetcode.raw_data, indent=2) if leetcode.raw_data else "Not available"}
"""
    else:
        prompt += "LeetCode data: NOT PROVIDED (This is okay - not all candidates use LeetCode)\n"
    
    if additional_context:
        prompt += f"\n=== ADDITIONAL CONTEXT ===\n{additional_context}\n"
    
    prompt += """

=== ANALYSIS TASK ===

Based on the above evidence, provide a detailed but supportive analysis in this EXACT JSON format:

{
    "confidence_level": "High | Medium | Low",
    "authenticity_score": <float 0-100>,
    "strong_evidence": [
        "List of skills/signals clearly supported by evidence",
        "Include specific examples (e.g., 'Python expertise shown in 15+ repos with recent activity')"
    ],
    "risk_indicators": [
        "Areas with weak or missing evidence",
        "Gaps that could be addressed with actionable steps",
        "Example: 'ML skills claimed but limited visible ML projects on GitHub'"
    ],
    "overall_assessment": "A 2-3 sentence neutral explanation of skill-evidence alignment. Supportive but honest.",
    "improvement_suggestions": [
        "Build a public project showcasing claimed skill X",
        "Add code samples or portfolio links to resume",
        "Document existing work with better READMEs",
        "Engage more consistently on GitHub",
        "Consider earning credentials in area Y"
    ],
    "skill_alignments": [
        {
            "skill": "Python",
            "confidence": "High | Medium | Low",
            "evidence_source": ["GitHub", "Projects", "LeetCode"],
            "supporting_evidence": [
                "Specific evidence like number of repos, problem types, etc."
            ],
            "gap_analysis": "What evidence is missing or weak for this skill, if any"
        }
    ]
}

CRITICAL GUIDELINES:
- confidence_level: Based on alignment strength (High=strong match, Medium=partial, Low=weak evidence)
- authenticity_score: 0-100 scale based on evidence comprehensiveness, NOT honesty judgment
- strong_evidence: Be SPECIFIC and ENCOURAGING about what IS shown
- risk_indicators: Frame as OPPORTUNITIES not accusations
- improvement_suggestions: Make them ACTIONABLE and ACHIEVABLE
- Do NOT penalize for missing GitHub/LeetCode - that's optional
- Do NOT assume missing evidence = dishonesty
- Tone: Professional, supportive, coaching-like

Output ONLY the JSON, no other text."""
    
    return prompt


# ==================== AGENT LOGIC ====================

async def analyze_authenticity(
    input_data: AuthenticityAnalysisInput | AuthenticityExtendedInput,
) -> AuthenticityExtendedOutput:
    """
    Main agent function: Analyze skill-evidence alignment.
    
    Returns supportive, ethical assessment with confidence levels and improvement suggestions.
    """
    
    # Validate resume text
    if input_data.resume and input_data.resume.raw_text:
        raw_text = input_data.resume.raw_text
        
        # Check for binary data in resume text
        if any(ord(c) < 32 and c not in '\n\r\t' for c in raw_text[:1000]):
            print("[Authenticity Agent] ERROR: Binary data detected in resume text")
            return _fallback_response(
                "Resume contains binary data. Please ensure text was properly extracted from PDF."
            )
        
        # Truncate very long text
        if len(raw_text) > 20000:
            print(f"[Authenticity Agent] WARNING: Resume text truncated from {len(raw_text)} to 20000 chars")
            input_data.resume.raw_text = raw_text[:20000] + "... [truncated]"
    
    # Generate analysis prompt
    system_prompt = _create_authenticity_system_prompt()
    analysis_prompt = _create_authenticity_analysis_prompt(
        resume=input_data.resume,
        github=input_data.github,
        leetcode=input_data.leetcode,
        additional_context=input_data.additional_context,
    )
    
    # Call LLM with strict JSON output requirement
    try:
        llm_response = await call_chat(
            prompt=system_prompt + "\n\n" + analysis_prompt,
            max_tokens=4000,  # Increased for complete response
            temperature=0.6,  # Slightly lower for more consistency
        )
        
        print(f"[Authenticity Agent] LLM Response length: {len(llm_response)}")
        print(f"[Authenticity Agent] LLM Response preview: {llm_response[:500]}...")
        
        # Parse JSON response
        analysis_result = _parse_json_response(llm_response)
        
        # Validate and construct output
        # Extract claims
        extracted_claims = _extract_claims(
            resume=input_data.resume,
            evidences=getattr(input_data, "evidences", []),
            github=input_data.github,
            leetcode=input_data.leetcode,
        )

        # Evidence mapping and verification
        claim_verifications = _verify_claims(
            claims=extracted_claims,
            evidences=getattr(input_data, "evidences", []),
        )

        output = AuthenticityExtendedOutput(
            confidence_level=analysis_result.get("confidence_level", "Medium"),
            authenticity_score=float(analysis_result.get("authenticity_score", 50)),
            strong_evidence=analysis_result.get("strong_evidence", []),
            risk_indicators=analysis_result.get("risk_indicators", []),
            overall_assessment=analysis_result.get("overall_assessment", "Analysis complete."),
            improvement_suggestions=analysis_result.get("improvement_suggestions", []),
            skill_alignments=_parse_skill_alignments(analysis_result.get("skill_alignments", [])),
            confidence_breakdown=analysis_result.get("confidence_breakdown", {}),
            extracted_claims=extracted_claims,
            claim_verifications=claim_verifications,
        )
        
        return output
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[Authenticity Agent] JSON parsing error: {e}")
        return _fallback_response(
            "Unable to parse LLM response. Returning default supportive assessment."
        )
    except Exception as e:
        print(f"[Authenticity Agent] Agent error: {e}")
        import traceback
        traceback.print_exc()
        return _fallback_response(
            f"Analysis encountered an issue: {str(e)}"
        )


# ==================== HELPER FUNCTIONS ====================

def _parse_json_response(response: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM response."""
    if not response or not response.strip():
        print("[Authenticity Agent] ERROR: Empty response from LLM")
        raise ValueError("Empty LLM response")
    
    # Try direct parse first
    try:
        parsed = json.loads(response)
        print(f"[Authenticity Agent] Successfully parsed JSON directly")
        return parsed
    except json.JSONDecodeError as e:
        print(f"[Authenticity Agent] Direct JSON parse failed: {e}")
    
    # Try extracting JSON block with markdown code blocks
    json_match = re.search(r'```json\s*({.*?})\s*```', response, re.DOTALL)
    if not json_match:
        json_match = re.search(r'```\s*({.*?})\s*```', response, re.DOTALL)
    if not json_match:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
    
    if json_match:
        try:
            parsed = json.loads(json_match.group(1) if len(json_match.groups()) > 0 else json_match.group(0))
            print(f"[Authenticity Agent] Successfully extracted and parsed JSON from response")
            return parsed
        except json.JSONDecodeError as e:
            print(f"[Authenticity Agent] JSON extraction parse failed: {e}")
    
    # Log the failure with more context
    print(f"[Authenticity Agent] ERROR: Could not parse JSON from response")
    print(f"[Authenticity Agent] Response preview: {response[:500]}")
    raise ValueError(f"Could not parse JSON from LLM response")


def _parse_skill_alignments(alignments_data: List[Dict[str, Any]]) -> List[SkillAlignment]:
    """Parse skill alignments from LLM output."""
    parsed = []
    for item in alignments_data:
        try:
            alignment = SkillAlignment(
                skill=item.get("skill", "Unknown"),
                confidence=item.get("confidence", "Medium"),
                evidence_source=item.get("evidence_source", []),
                supporting_evidence=item.get("supporting_evidence", []),
                gap_analysis=item.get("gap_analysis"),
            )
            parsed.append(alignment)
        except Exception as e:
            print(f"Error parsing skill alignment: {e}")
    return parsed


def _fallback_response(message: str) -> AuthenticityExtendedOutput:
    """Generate supportive fallback response."""
    return AuthenticityExtendedOutput(
        confidence_level="Medium",
        authenticity_score=50,
        strong_evidence=[
            "Resume data received and ready for analysis"
        ],
        risk_indicators=[
            "Limited external evidence provided for detailed analysis"
        ],
        overall_assessment=f"{message} We recommend providing GitHub profile and project links for a more comprehensive assessment.",
        improvement_suggestions=[
            "Share your GitHub profile URL for deeper analysis",
            "Link to your project portfolio or personal website",
            "If applicable, share LeetCode or coding challenge profiles",
            "Document your contributions with clear project descriptions",
        ],
        extracted_claims=[],
        claim_verifications=[],
    )


# ==================== CLAIM EXTRACTION & VERIFICATION ====================

def _extract_claims(
    resume: ResumeData,
    evidences: List[EvidenceItem],
    github: Optional[GitHubEvidence] = None,
    leetcode: Optional[LeetCodeEvidence] = None,
) -> List[Claim]:
    claims: List[Claim] = []
    # Skills
    for s in resume.skills or []:
        claims.append(Claim(kind="skill", text=s, normalized=s.lower(), source="resume"))
    # Certifications
    for c in resume.certifications or []:
        claims.append(Claim(kind="certification", text=c, normalized=c.lower(), source="resume"))
    # Projects
    for p in resume.projects or []:
        name = str(p.get("name") or p.get("title") or "Project").strip()
        claims.append(Claim(kind="project", text=name, normalized=name.lower(), source="resume"))
    # Participation (hackathons)
    for exp in resume.experience or []:
        desc = str(exp.get("description") or "").lower()
        if "hackathon" in desc:
            claims.append(Claim(kind="participation", text=exp.get("description", "Hackathon participation"), source="resume"))
    # Usernames from resume links (implicit evidence)
    for section in [resume.raw_text or ""]:
        for platform in ["github", "leetcode", "kaggle", "codeforces", "hackerrank"]:
            for m in re.findall(rf"{platform}\.com/([A-Za-z0-9_-]+)", section, re.IGNORECASE):
                claims.append(Claim(kind="username", text=f"{platform}:{m}", normalized=m.lower(), source="resume"))
    # Evidence metadata-derived claims
    for ev in evidences or []:
        if ev.type in ["github_profile", "leetcode_profile", "kaggle"] and ev.url:
            uname = ev.url.split("/")[-1]
            claims.append(Claim(kind="username", text=f"{ev.type}:{uname}", normalized=uname.lower(), source="evidence", extracted_from=ev.url))
        if ev.type == "certificate" and ev.title:
            claims.append(Claim(kind="certification", text=ev.title, normalized=ev.title.lower(), source="evidence", extracted_from=ev.url))
        if ev.type == "github_repo" and ev.title:
            claims.append(Claim(kind="project", text=ev.title, normalized=ev.title.lower(), source="evidence", extracted_from=ev.url))
    return claims


def _verify_claims(
    claims: List[Claim],
    evidences: List[EvidenceItem],
) -> List[ClaimVerification]:
    results: List[ClaimVerification] = []
    for claim in claims:
        mapped: List[ClaimEvidenceMapping] = []
        # Simple heuristic mapping by type/text match
        for ev in evidences or []:
            rel = _estimate_relevance(claim, ev)
            if rel <= 0:
                continue
            strength = _estimate_strength(claim, ev)
            direct = _estimate_directness(claim, ev)
            mapped.append(ClaimEvidenceMapping(evidence=ev, relevance=rel, strength=strength, directness=direct))

        # Determine status and confidence
        if not mapped:
            status = "Unverified"
            conf = 20.0
        else:
            avg_strength = sum(m.strength for m in mapped) / len(mapped)
            avg_direct = sum(m.directness for m in mapped) / len(mapped)
            avg_rel = sum(m.relevance for m in mapped) / len(mapped)
            score = (0.4 * avg_strength + 0.4 * avg_direct + 0.2 * avg_rel) * 100
            conf = max(10.0, min(95.0, score))
            if avg_strength > 0.7 and avg_direct > 0.7:
                status = "Verified"
            elif avg_strength > 0.4 or avg_direct > 0.4:
                status = "Partially Verified"
            else:
                status = "Unverified"

        # RAG checks placeholder (strict: inconclusive if none)
        rag_notes: List[str] = []
        flags: List[str] = []
        if claim.kind == "certification":
            rag_notes.append("Certification issuer check pending via RAG")
        if claim.kind == "participation":
            rag_notes.append("Hackathon legitimacy check pending via RAG")

        results.append(ClaimVerification(
            claim=claim,
            status=status,
            confidence=conf,
            mapped_evidence=mapped,
            rag_checks=rag_notes,
            flags=flags,
        ))
    return results


def _estimate_relevance(claim: Claim, ev: EvidenceItem) -> float:
    if claim.kind == "skill" and ev.type in ["github_repo", "github_profile", "portfolio", "blog"]:
        text = (ev.title or "") + " " + (ev.description or "")
        return 0.8 if claim.text.lower() in text.lower() else 0.3
    if claim.kind == "certification" and ev.type == "certificate":
        return 0.9 if (ev.title or "").lower().find(claim.text.lower()) >= 0 else 0.4
    if claim.kind == "project" and ev.type == "github_repo":
        return 0.9 if (ev.title or "").lower().find(claim.text.lower()) >= 0 else 0.5
    if claim.kind == "username" and ev.url:
        return 0.9 if claim.normalized and claim.normalized in ev.url.lower() else 0.4
    return 0.2


def _estimate_strength(claim: Claim, ev: EvidenceItem) -> float:
    # Use metadata hints if available
    stars = int(ev.metadata.get("stars", 0))
    commits = int(ev.metadata.get("commits", 0))
    readme = ev.metadata.get("readme_quality", "")
    if ev.type == "github_repo":
        base = 0.5 + min(stars, 100) / 200
        base += 0.2 if commits > 20 else 0.0
        base += 0.2 if str(readme).lower() in ["good", "excellent"] else 0.0
        return min(1.0, base)
    if ev.type == "certificate":
        return 0.8 if ev.metadata.get("issuer_verified") else 0.5
    if ev.type in ["leetcode_profile", "kaggle"]:
        solved = int(ev.metadata.get("problems_solved", 0))
        return 0.3 + min(solved, 300) / 1000
    return 0.4


def _estimate_directness(claim: Claim, ev: EvidenceItem) -> float:
    if claim.kind == "skill" and ev.type == "github_repo":
        # Direct when repo demonstrates the skill explicitly
        text = (ev.title or "") + " " + (ev.description or "")
        return 0.8 if claim.text.lower() in text.lower() else 0.5
    if claim.kind == "certification" and ev.type == "certificate":
        return 0.95
    if claim.kind == "project" and ev.type == "github_repo":
        return 0.85
    if claim.kind == "participation" and ev.type == "link":
        return 0.6
    return 0.4


def _calculate_confidence_metrics(
    resume: ResumeData,
    github: Optional[GitHubEvidence] = None,
    leetcode: Optional[LeetCodeEvidence] = None,
) -> Dict[str, Any]:
    """Calculate internal confidence metrics (for debugging/logging)."""
    metrics = {
        "resume_completeness": 0,
        "github_strength": 0,
        "evidence_diversity": 0,
    }
    
    # Resume completeness
    resume_score = 0
    if resume.skills:
        resume_score += 20
    if resume.experience:
        resume_score += 20
    if resume.projects:
        resume_score += 20
    if resume.education:
        resume_score += 20
    if resume.raw_text:
        resume_score += 20
    metrics["resume_completeness"] = min(100, resume_score)
    
    # GitHub strength
    if github:
        github_score = 0
        if github.languages:
            github_score += 25
        if github.repo_count >= 5:
            github_score += 25
        if github.contribution_pattern in ["consistent", "high"]:
            github_score += 25
        if github.readme_quality in ["good", "excellent"]:
            github_score += 25
        metrics["github_strength"] = min(100, github_score)
    
    # Evidence diversity
    evidence_count = sum([
        1 if resume else 0,
        1 if github else 0,
        1 if leetcode and leetcode.problems_solved > 0 else 0,
    ])
    metrics["evidence_diversity"] = (evidence_count / 3) * 100
    
    return metrics
