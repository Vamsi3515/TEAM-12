# Experience Authenticity & Skill Consistency Agent

## Overview

The **Experience Authenticity & Skill Consistency Agent** is an AI-powered decision-support system that analyzes the alignment between a candidate's resume claims and observable evidence (GitHub, LeetCode, etc.) to generate confidence and risk signals about employability readiness.

### Key Principle
This is **NOT a fraud detector**. It's a **supportive, ethical agent** that helps candidates understand skill alignment and provides actionable improvement suggestions.

---

## Core Values

✅ **Supportive** - Candidate-friendly, encouraging tone  
✅ **Ethical** - Never assumes missing evidence = dishonesty  
✅ **Explainable** - Clear reasoning for each assessment  
✅ **Non-Accusatory** - Professional, neutral language  
✅ **Improvement-Focused** - Actionable next steps  

---

## What the Agent Does

### Analyzes
- **Resume claims** (skills, experience, projects, education)
- **GitHub evidence** (languages, repos, commits, README quality, contribution patterns)
- **LeetCode stats** (problems solved, difficulty distribution, activity)
- **Code quality** (architecture, documentation, project maturity)

### Generates
- **Confidence Level** - How well evidence supports resume claims (High/Medium/Low)
- **Authenticity Score** - 0-100 metric based on evidence comprehensiveness
- **Strong Evidence** - Skills clearly supported with specific examples
- **Risk Indicators** - Weak or missing evidence areas (framed as opportunities)
- **Overall Assessment** - Short, neutral explanation of alignment
- **Improvement Suggestions** - Actionable steps to strengthen portfolio
- **Skill Alignments** - Detailed skill-by-skill analysis

### Does NOT Do
- ❌ Assume missing evidence = dishonesty
- ❌ Penalize candidates for lacking GitHub/LeetCode
- ❌ Make hiring decisions
- ❌ Rank candidates
- ❌ Use accusatory language ("fraud", "fake", "deceptive", etc.)

---

## API Endpoint

### POST `/api/analyze-authenticity`

Analyzes skill consistency between resume and observable evidence.

#### Request Body

```json
{
  "resume": {
    "full_name": "string (optional)",
    "skills": ["Python", "React", "FastAPI", ...],
    "experience": [
      {
        "title": "Backend Engineer",
        "company": "TechCorp",
        "duration": "2 years",
        "description": "Optional description"
      }
    ],
    "projects": [
      {
        "name": "Project Name",
        "description": "Project description"
      }
    ],
    "education": [
      {
        "degree": "BS Computer Science",
        "school": "University Name",
        "year": 2021
      }
    ],
    "certifications": ["AWS Solutions Architect", ...],
    "raw_text": "Full resume text (optional)"
  },
  "github": {
    "username": "github-username (optional)",
    "languages": ["Python", "JavaScript", ...],
    "repo_count": 28,
    "commit_frequency": "consistent | sporadic | recent | high | low",
    "top_projects": [
      {
        "name": "project-name",
        "description": "Project description",
        "stars": 45,
        "languages": ["Python"],
        "updated": "1 week ago",
        "readme_quality": "excellent | good | fair | poor"
      }
    ],
    "readme_quality": "excellent | good | fair | poor",
    "contribution_pattern": "consistent | sporadic | recent",
    "raw_profile_data": {} // Optional detailed GitHub API response
  },
  "leetcode": {
    "problems_solved": 187,
    "difficulty_distribution": {
      "Easy": 65,
      "Medium": 89,
      "Hard": 33
    },
    "recent_activity": true,
    "ranking": "Top 15% (optional)"
  },
  "additional_context": "Any other relevant information (optional)"
}
```

#### Response Body (Strict JSON)

```json
{
  "confidence_level": "High | Medium | Low",
  "authenticity_score": 85,
  "strong_evidence": [
    "Python expertise clearly demonstrated: 28 GitHub repos with consistent commits",
    "FastAPI mastery: Production-grade APIs with excellent documentation",
    "Strong problem-solving: 187 LeetCode problems solved"
  ],
  "risk_indicators": [
    "Limited ML project visibility for claimed data science skills",
    "Could strengthen AWS expertise with infrastructure examples"
  ],
  "overall_assessment": "Excellent alignment between resume claims and GitHub evidence. Strong technical foundation with consistent contributions and well-documented projects.",
  "improvement_suggestions": [
    "Build 1-2 public ML projects to showcase data science skills",
    "Create detailed architecture documentation for complex systems",
    "Maintain consistent GitHub activity to demonstrate ongoing learning"
  ],
  "skill_alignments": [
    {
      "skill": "Python",
      "confidence": "High",
      "evidence_source": ["GitHub", "LeetCode"],
      "supporting_evidence": [
        "28 repositories using Python",
        "187 LeetCode problems solved"
      ],
      "gap_analysis": null
    },
    {
      "skill": "Machine Learning",
      "confidence": "Low",
      "evidence_source": ["Resume"],
      "supporting_evidence": [],
      "gap_analysis": "Claimed in resume but limited visible ML projects on GitHub"
    }
  ]
}
```

---

## Use Cases

### 1. Resume Screening Enhancement
Help recruiters understand skill alignment without bias, focusing on evidence over keywords.

### 2. Candidate Self-Assessment
Allow candidates to understand how their portfolio supports their claims and identify improvement areas.

### 3. Career Development Guidance
Provide actionable suggestions for strengthening employability evidence.

### 4. Interview Preparation
Guide candidates on which projects to highlight and what evidence gaps to address.

### 5. Skills Gap Analysis
Identify which claimed skills lack public evidence and suggest ways to demonstrate them.

---

## Confidence Level Interpretation

### High (85-100)
- Strong, consistent evidence across multiple sources
- Resume claims well-supported by visible projects
- Demonstrated active learning and engagement
- Clear skill-to-evidence alignment

**Example**: Multiple well-documented GitHub repos, consistent commits, strong LeetCode presence, certifications

### Medium (50-84)
- Partial evidence or mixed signals
- Some claims well-supported, others lacking visibility
- Limited but reasonable evidence base
- Opportunity for improvement

**Example**: Good GitHub presence but repos lack documentation, or strong resume with sporadic commit history

### Low (0-49)
- Limited or weak evidence
- Claims not well-supported by observable evidence
- Significant gaps that could be addressed
- Early-career or no public portfolio

**Example**: Strong resume claims with minimal GitHub presence, no supporting code or projects

---

## Authenticity Score Breakdown

The 0-100 score reflects **evidence comprehensiveness**, NOT honesty or integrity:

- **0-20**: Minimal evidence provided (e.g., resume only, no GitHub/LeetCode)
- **20-40**: Limited evidence with gaps (e.g., sparse GitHub activity, low LeetCode problems)
- **40-60**: Moderate evidence (partial support, some gaps) 
- **60-80**: Good evidence (most skills supported, minor gaps)
- **80-100**: Comprehensive evidence (strong support across multiple sources)

### What the Score Does NOT Mean
- 100 ≠ "Perfect candidate" - just well-documented skills
- 50 ≠ "Dishonest" - just limited public evidence
- Low score ≠ Unqualified - external constraints limit visibility

---

## Example Scenarios

### Scenario 1: Strong Alignment
```
Resume: Claims Python, FastAPI, DevOps expertise
GitHub: 
  - 25 repos with Python, FastAPI, Docker
  - Consistent commits (5+ per week)
  - Well-documented projects with high stars
  - READMEs explain architecture decisions

Result: 
  - Confidence: High
  - Score: 88
  - Assessment: "Claims well-supported by strong evidence"
  - Suggestion: "Maintain momentum; document new projects thoroughly"
```

### Scenario 2: Weak Alignment
```
Resume: Claims ML/AI expertise, deep TensorFlow knowledge
GitHub:
  - Only tutorial/example notebooks
  - Few original ML projects
  - No architecture documentation
  - Sporadic commits (1-2 per month)

Result:
  - Confidence: Low
  - Score: 42
  - Assessment: "Limited visible evidence for ML claims"
  - Suggestion: "Build original ML project with clear documentation"
```

### Scenario 3: No GitHub
```
Resume: 5+ years at large enterprise
Context: "Proprietary financial systems, limited open-source work"
LeetCode: Not provided
GitHub: None

Result:
  - Confidence: Medium
  - Score: 65
  - Assessment: "Resume credible; enterprise background explains limited GitHub"
  - Suggestion: "Build side projects to demonstrate portfolio capability"
```

---

## Important Notes

### Missing Evidence ≠ Dishonesty
- Many roles (especially in regulated industries) involve proprietary code
- Not everyone uses LeetCode or maintains GitHub
- Some candidates are early-career with limited history
- Enterprise work may not translate to public portfolio

### The Agent Supports, Not Judges
- Never assumes absence of evidence = negative intent
- Recognizes legitimate constraints on code sharing
- Provides constructive, actionable feedback
- Respects privacy and career circumstances

### Candidate-First Philosophy
- Helps candidates understand their strengths
- Identifies specific, achievable improvements
- Encourages portfolio building without accusation
- Supportive tone throughout

---

## Integration with Multi-Agent System

The Authenticity Agent works with:
- **ATS Analyzer** - Resume keyword matching and formatting
- **GitHub Analyzer** - Repository analysis and tech stack detection
- **Resume Parser** - Structured resume extraction
- **Interview Prep** - Use evidence gaps for interview coaching

Together, they provide comprehensive employability analysis without replacing human judgment.

---

## Technical Implementation

### Framework
- **FastAPI** - REST API
- **Pydantic** - Schema validation
- **Gemini/Groq/OpenAI** - LLM for analysis

### Key Components
1. **Prompt Engineering** - Ethical, supportive system prompts
2. **JSON Schema** - Strict output format
3. **Error Handling** - Graceful fallbacks
4. **Logging** - Transparency in reasoning

### Customization
Modify `_create_authenticity_system_prompt()` in `authenticity_agent.py` to:
- Adjust evaluation criteria
- Change tone or emphasis
- Add domain-specific logic
- Customize output format

---

## Privacy & Ethics

✅ Does not store personal data  
✅ Analysis is local to request/response  
✅ No candidate profiling or ranking  
✅ No hiring decisions made  
✅ Transparent reasoning shown in output  
✅ Respects career stage and circumstances  

---

## Questions & Feedback

For issues or improvements:
1. Check error messages in response
2. Review agent prompts if output is biased
3. Add more context if analysis seems incomplete
4. Consider candidate circumstances (industry, career stage, background)

---

## Related Documentation

- [ATS Analyzer](../README_EVALS.md)
- [GitHub Analyzer](../README_EVALS.md)
- [API Examples](./authenticity_examples.py)
- [Evaluation Metrics](./eval_metrics.py)
