# Experience Authenticity Agent - Visual Guides & Diagrams

## 🎯 Agent Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│     EXPERIENCE AUTHENTICITY & SKILL CONSISTENCY AGENT           │
│                                                                 │
│              A Supportive Decision-Support System               │
│                      (NOT a Fraud Detector)                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       INPUT DATA                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📄 RESUME                  🐙 GITHUB              🧮 LEETCODE │
│  ├─ Skills                  ├─ Languages          ├─ Problems  │
│  ├─ Experience              ├─ Repos              ├─ Difficulty│
│  ├─ Projects                ├─ Commits            └─ Activity  │
│  ├─ Education               ├─ Docs Quality                    │
│  └─ Certifications          └─ Contribution                    │
│                                Pattern                          │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────▼─────────────┐
                │  DATA EXTRACTION &       │
                │  VALIDATION (Pydantic)   │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │  PROMPT ENGINEERING     │
                │  - System Prompt        │
                │  - Analysis Prompt      │
                │  - Ethical Safeguards   │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │  LLM API CALL           │
                │  - Gemini / Groq        │
                │  - OpenAI / HuggingFace │
                │  - JSON Response Mode   │
                └────────────┬─────────────┘
                             │
                ┌────────────▼─────────────┐
                │  RESPONSE PARSING       │
                │  - Extract JSON         │
                │  - Validate Structure   │
                │  - Fallback Handler     │
                └────────────┬─────────────┘
                             │
┌─────────────────────────────▼─────────────────────────────────┐
│                       OUTPUT DATA                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 CONFIDENCE LEVEL        🎯 AUTHENTICITY SCORE            │
│  ├─ High (85-100)           ├─ 0-100 Scale                  │
│  ├─ Medium (50-84)          └─ Evidence Comprehensiveness   │
│  └─ Low (0-49)                                              │
│                                                              │
│  ✅ STRONG EVIDENCE         ⚠️  RISK INDICATORS             │
│  ├─ Supported Skills        ├─ Weak Evidence Areas          │
│  ├─ Positive Signals        ├─ Framed as Opportunities      │
│  └─ Clear Examples          └─ No Judgment                  │
│                                                              │
│  📝 OVERALL ASSESSMENT      💡 IMPROVEMENT SUGGESTIONS       │
│  ├─ Neutral Explanation     ├─ Actionable Steps             │
│  ├─ Supportive Tone         ├─ Specific Recommendations     │
│  └─ Evidence Mapping        └─ Encouraging Framing          │
│                                                              │
│  🔍 SKILL ALIGNMENTS (Detailed Analysis)                    │
│  ├─ Per-Skill Confidence                                   │
│  ├─ Evidence Mapping                                       │
│  └─ Gap Analysis                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Architecture

```
                    ┌─────────────────────┐
                    │   User Request      │
                    │ (Resume + GitHub +  │
                    │  LeetCode)          │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    ┌────────┐         ┌───────────┐         ┌──────────┐
    │ Resume │         │  GitHub   │         │ LeetCode │
    │ Data   │         │  Profile  │         │  Stats   │
    └────┬───┘         └─────┬─────┘         └────┬─────┘
         │                   │                    │
         │  ResumeData       │  GitHubEvidence   │  LeetCodeEvidence
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ AuthenticityAnalysis
                    │ Input (combined) │
                    └────────┬────────┘
                             │
                ┌────────────▼────────────┐
                │ analyze_authenticity() │
                │ (Core Agent Logic)      │
                └────────────┬────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌─────────┐         ┌─────────┐         ┌──────────┐
    │ System  │         │ Analysis│         │ Fallback │
    │ Prompt  │         │ Prompt  │         │ Response │
    └─────┬───┘         └────┬────┘         └────┬─────┘
          │                  │                   │
          └──────────┬───────┘                   │
                     │                           │
            ┌────────▼─────────┐                │
            │  LLM Call        │                │
            │  (JSON Mode)     │                │
            └────────┬─────────┘                │
                     │                           │
        ┌────────────▼───────────┐              │
        │ JSON Response Parsing   │              │
        │ - Extract JSON          │              │
        │ - Handle Malformed      │              │
        │ - Retry if needed       │              │
        └────────────┬────────────┘              │
                     │                           │
        ┌────────────▼────────────┐  ┌───────────▼────────┐
        │ Success: Valid JSON     │  │ Error: Use Fallback│
        │ (All 6 fields present)  │  │ (Generated response)
        └────────────┬────────────┘  └───────────┬────────┘
                     │                           │
                     └───────────┬───────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ AuthenticityAnalysis    │
                    │ Output (Final)          │
                    │ - confidence_level      │
                    │ - authenticity_score    │
                    │ - strong_evidence       │
                    │ - risk_indicators       │
                    │ - overall_assessment    │
                    │ - improvement_suggest   │
                    │ - skill_alignments      │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Return to Client        │
                    │ (JSON Response)         │
                    └─────────────────────────┘
```

---

## 📊 Confidence Level Matrix

```
CONFIDENCE LEVEL INTERPRETATION

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  HIGH (85-100)                                              │
│  ═══════════════════════════════════════════════════════    │
│  Meaning: Strong evidence alignment                         │
│  Examples:                                                  │
│  • 20+ GitHub repos with claimed skills                    │
│  • Consistent commit patterns (5+ per week)                │
│  • Well-documented projects                                │
│  • Certifications or LeetCode support                      │
│  • Clear skill-to-project mapping                          │
│                                                              │
│  MEDIUM (50-84)                                             │
│  ═════════════════════════════════════════════════════     │
│  Meaning: Partial evidence or mixed signals                │
│  Examples:                                                  │
│  • Some skills well-supported, others weak                 │
│  • Limited GitHub presence but strong resume              │
│  • Sporadic commits but quality projects                  │
│  • Early-career with growing portfolio                    │
│  • Enterprise background with limited public code         │
│                                                              │
│  LOW (0-49)                                                │
│  ═════════════════════════════════════════════════════    │
│  Meaning: Limited or weak evidence                         │
│  Examples:                                                  │
│  • Claims without visible support                          │
│  • No GitHub/LeetCode/portfolio provided                 │
│  • Very early career with no public work                  │
│  • Limited documentation or explanation                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘

AUTHENTICITY SCORE BREAKDOWN

0-20    │ ▓ Minimal evidence (resume only)
        │
20-40   │ ▓▓ Limited evidence (sparse activity)
        │
40-60   │ ▓▓▓ Moderate evidence (partial support)
        │
60-80   │ ▓▓▓▓ Good evidence (most skills supported)
        │
80-100  │ ▓▓▓▓▓ Comprehensive evidence (strong across sources)
        │
```

---

## 🎯 Use Case Scenarios

```
SCENARIO 1: STRONG EVIDENCE CANDIDATE
════════════════════════════════════════════════════════════════

Resume Claims:          Observable Evidence:        Result:
┌──────────────┐        ┌──────────────────┐        ┌─────────┐
│ Python       │ ───→   │ 25 GitHub repos  │ ──→    │ HIGH    │
│ FastAPI      │ ───→   │ Consistent commits          │ 88/100  │
│ React        │ ───→   │ Excellent READMEs           │         │
│ DevOps       │ ───→   │ Docker/K8s projects         │ ✓ Match │
└──────────────┘        └──────────────────┘        └─────────┘

Feedback: "Excellent alignment. Keep building! 🚀"


SCENARIO 2: PARTIAL EVIDENCE CANDIDATE
════════════════════════════════════════════════════════════════

Resume Claims:          Observable Evidence:        Result:
┌──────────────┐        ┌──────────────────┐        ┌─────────┐
│ Machine      │ ───→   │ 3 GitHub repos   │ ──→    │ MEDIUM  │
│ Learning     │ ───→   │ Sparse commits               │ 58/100  │
│ TensorFlow   │ ───→   │ Fair documentation          │         │
│ Data Science │        │ Limited ML projects         │ ⚠ Gap   │
└──────────────┘        └──────────────────┘        └─────────┘

Feedback: "Resume credible. Build public ML projects to strengthen. 💡"


SCENARIO 3: NO PUBLIC PORTFOLIO
════════════════════════════════════════════════════════════════

Resume Claims:          Observable Evidence:        Result:
┌──────────────┐        ┌──────────────────┐        ┌─────────┐
│ Senior Eng   │ ───→   │ No GitHub        │ ──→    │ MEDIUM  │
│ Microservices│ ───→   │ 4+ yrs experience            │ 72/100  │
│ AWS/K8s      │ ───→   │ Certifications              │         │
│ Java/Spring  │        │ Enterprise background       │ No Data │
└──────────────┘        └──────────────────┘        └─────────┘

Feedback: "Experience credible. Consider building public examples. 👍"
```

---

## 🧠 LLM Prompt Strategy

```
SYSTEM PROMPT STRUCTURE
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ 1. IDENTITY & ROLE                                          │
│    "You are an Experience Authenticity Agent..."            │
│                                                              │
│ 2. CRITICAL PRINCIPLES                                      │
│    "Do NOT assume missing evidence = dishonesty"            │
│    "Do NOT penalize for no GitHub/LeetCode"                │
│    "Do NOT use accusatory language"                         │
│                                                              │
│ 3. TONE REQUIREMENT                                         │
│    "Supportive, professional, non-judgmental"              │
│    "Candidate-friendly and encouraging"                    │
│                                                              │
│ 4. ANALYSIS GUIDELINES                                      │
│    "Identify clearly supported skills"                     │
│    "Flag weak evidence as opportunities"                   │
│    "Suggest actionable improvements"                       │
│                                                              │
│ 5. OUTPUT FORMAT                                            │
│    "STRICT JSON ONLY"                                      │
│    "No extra text"                                         │
│    "All 6 required fields present"                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

ANALYSIS PROMPT STRUCTURE
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ SECTION 1: RESUME DATA                                      │
│   ├─ Skills claimed                                         │
│   ├─ Experience history                                     │
│   ├─ Projects listed                                        │
│   └─ Raw text (if available)                               │
│                                                              │
│ SECTION 2: GITHUB EVIDENCE                                  │
│   ├─ Languages used                                         │
│   ├─ Repository details                                     │
│   ├─ Contribution patterns                                  │
│   └─ Documentation quality                                  │
│                                                              │
│ SECTION 3: LEETCODE EVIDENCE                                │
│   ├─ Problems solved                                        │
│   ├─ Difficulty distribution                                │
│   └─ Activity level                                         │
│                                                              │
│ SECTION 4: ADDITIONAL CONTEXT                               │
│   └─ Any other relevant information                         │
│                                                              │
│ SECTION 5: ANALYSIS TASK                                    │
│   ├─ Generate JSON response                                 │
│   ├─ Include specific examples                              │
│   └─ Frame gaps constructively                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Response Structure Diagram

```
STRICT JSON OUTPUT FORMAT
═══════════════════════════════════════════════════════════════

{
    ┌─────────────────────────────────────────────────────────┐
    │ confidence_level                                        │
    │   "High" | "Medium" | "Low"                            │
    │   ↳ Based on evidence alignment strength               │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ authenticity_score                                      │
    │   0.0 - 100.0                                          │
    │   ↳ Evidence comprehensiveness (NOT honesty judgment)   │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ strong_evidence                                         │
    │   [                                                     │
    │     "Skill A: specific evidence with examples",        │
    │     "Skill B: clear examples and metrics",             │
    │     ...                                                │
    │   ]                                                     │
    │   ↳ Supported skills with specific details             │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ risk_indicators                                         │
    │   [                                                     │
    │     "Limited visible evidence for skill X",            │
    │     "Gap between claim Y and observable evidence",     │
    │     ...                                                │
    │   ]                                                     │
    │   ↳ Weak areas framed as OPPORTUNITIES                │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ overall_assessment                                      │
    │   "2-3 sentence neutral summary"                       │
    │   ↳ Supportive, professional, non-accusatory           │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ improvement_suggestions                                 │
    │   [                                                     │
    │     "Build public project showcasing skill X",         │
    │     "Improve documentation on existing projects",      │
    │     "Consider earning credential in area Y",           │
    │     ...                                                │
    │   ]                                                     │
    │   ↳ ACTIONABLE, SPECIFIC, ENCOURAGING                  │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │ skill_alignments (OPTIONAL - Detailed Analysis)         │
    │   [                                                     │
    │     {                                                   │
    │       "skill": "Python",                               │
    │       "confidence": "High",                            │
    │       "evidence_source": ["GitHub", "LeetCode"],      │
    │       "supporting_evidence": ["20 repos", "..."],     │
    │       "gap_analysis": null or "description"            │
    │     },                                                  │
    │     ...                                                │
    │   ]                                                     │
    │   ↳ Per-skill breakdown with specific mapping          │
    └─────────────────────────────────────────────────────────┘
}
```

---

## 🔒 Ethical Safeguards Checklist

```
LANGUAGE SAFEGUARDS
═══════════════════════════════════════════════════════════════

✅ DO USE                          ❌ NEVER USE
───────────────────────────────────────────────────────────────
Opportunity to strengthen          Fraud / Fake
Limited visible evidence           Dishonest / Deceptive
Consider building a project        False claims / Liar
Gap between claim and evidence     Red flag / Suspicious
Would benefit from more            Caught them in
Evidence is weak in area X         Doesn't match
Portfolio could be stronger        Exposed

RESPONSE VALIDATION CHECKLIST
═══════════════════════════════════════════════════════════════

Before returning response:
☑ No forbidden words found
☑ Positive framing used
☑ JSON structure valid
☑ All required fields present
☑ Score between 0-100
☑ Confidence level valid
☑ Suggestions are actionable
☑ Tone is supportive
```

---

## 🚀 Integration Patterns

```
PATTERN 1: SEQUENTIAL ANALYSIS
═══════════════════════════════════════════════════════════════

Resume Text
    ↓
Parse Resume → Extract Structured Data
    ↓
Fetch GitHub → Analyze Repository Data
    ↓
Fetch LeetCode → Get Problem Stats
    ↓
Combine Evidence → Create Input
    ↓
Call Authenticity Agent
    ↓
Return Result


PATTERN 2: PARALLEL ANALYSIS
═══════════════════════════════════════════════════════════════

Resume Text ──┐
              ├→ Parallel Processing ──→ Combine Data ──→ Agent
GitHub URL ──┤
              ├→
LeetCode ID ─┤


PATTERN 3: OPTIONAL GITHUB/LEETCODE
═══════════════════════════════════════════════════════════════

Resume Text
    ↓
Try: Fetch GitHub → Success? Use Data : Skip
    ↓
Try: Fetch LeetCode → Success? Use Data : Skip
    ↓
Combine Available Data
    ↓
Call Agent with What You Have
    ↓
Agent Handles Gracefully
```

---

## 📊 Example Output Visualization

```
CANDIDATE: ALICE JOHNSON
═══════════════════════════════════════════════════════════════

Confidence Level:
  ████████░ HIGH (88/100)

Authenticity Score:
  ██████████ 88/100

Strong Evidence:          Risk Indicators:
✅ Python expertise      ⚠️  Limited ML projects
✅ FastAPI mastery       ⚠️  Could strengthen AWS
✅ Consistent commits
✅ Excellent docs

Overall Assessment:
"Excellent alignment between resume claims and GitHub evidence. 
Strong track record with well-documented projects. Consistent 
learning and engagement demonstrated."

Improvement Suggestions:
💡 Build 1-2 AWS-focused projects
💡 Document architecture decisions
💡 Maintain commit momentum


CANDIDATE: BOB SMITH
═══════════════════════════════════════════════════════════════

Confidence Level:
  █████░░░░ MEDIUM (58/100)

Authenticity Score:
  ██████░░░ 58/100

Strong Evidence:          Risk Indicators:
✅ MS in Data Science     ⚠️  Limited public ML projects
✅ Relevant work history  ⚠️  Sporadic GitHub activity

Overall Assessment:
"Resume credible, but portfolio could better demonstrate claimed 
ML expertise. Enterprise background explains limited public code. 
Focus on building visible proof of capabilities."

Improvement Suggestions:
💡 Build public ML project with documentation
💡 Share Kaggle competitions
💡 Improve README quality
💡 More consistent GitHub engagement
```

---

## 🎓 Key Takeaways

```
THE 5 CORE PRINCIPLES
═══════════════════════════════════════════════════════════════

1. SUPPORT OVER JUDGMENT
   Candidate Coach, Not Accuser

2. EVIDENCE OVER ASSUMPTION
   Based on Observable Facts

3. GROWTH OVER CRITICISM
   Opportunity-Focused Framing

4. RESPECT OVER PRESSURE
   Acknowledge Constraints

5. TRANSPARENCY OVER OPACITY
   Clear Reasoning Shown
```

---

**For more details, refer to:**
- Complete Guide: `AUTHENTICITY_AGENT_GUIDE.md`
- Quick Reference: `AUTHENTICITY_QUICK_REFERENCE.md`
- Integration: `AUTHENTICITY_INTEGRATION_GUIDE.md`
