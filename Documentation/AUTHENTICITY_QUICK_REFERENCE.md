# Experience Authenticity & Skill Consistency Agent - Quick Reference

## 🎯 What It Is
A **supportive decision-support system** that analyzes skill alignment between resume claims and observable evidence (GitHub, LeetCode). **NOT a fraud detector.**

## 📊 Output Format

```json
{
  "confidence_level": "High | Medium | Low",
  "authenticity_score": 0-100,
  "strong_evidence": ["Supported skills..."],
  "risk_indicators": ["Areas for improvement..."],
  "overall_assessment": "Summary explanation",
  "improvement_suggestions": ["Actionable steps..."]
}
```

## 🚀 Quick Start

### API Endpoint
```bash
POST /api/analyze-authenticity
```

### Minimal Request
```json
{
  "resume": {
    "skills": ["Python", "React", "Docker"],
    "experience": [{"title": "Engineer", "company": "TechCorp"}]
  }
}
```

### Detailed Request
```json
{
  "resume": {
    "full_name": "Alice Johnson",
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "experience": [{...}],
    "projects": [{...}],
    "education": [{...}],
    "certifications": ["AWS Associate"],
    "raw_text": "Full resume content"
  },
  "github": {
    "username": "alice-dev",
    "languages": ["Python", "JavaScript"],
    "repo_count": 25,
    "commit_frequency": "consistent",
    "top_projects": [{...}],
    "readme_quality": "excellent",
    "contribution_pattern": "consistent"
  },
  "leetcode": {
    "problems_solved": 187,
    "difficulty_distribution": {"Easy": 65, "Medium": 89, "Hard": 33},
    "recent_activity": true
  },
  "additional_context": "Optional notes about the candidate"
}
```

## 🎨 Tone & Language

### ✅ DO Use
- "Opportunity to strengthen evidence"
- "Limited visible evidence for this skill"
- "Consider building a public project"
- "Well-supported by GitHub activity"
- "Strong foundation with opportunities to expand"

### ❌ DON'T Use
- "Fraudulent", "fake", "dishonest"
- "Red flag", "suspicious", "doesn't match"
- "Lying about skills", "false claims"
- "Caught them in", "exposed"

## 📈 Confidence Level Guide

| Level | Score | Meaning | Example |
|-------|-------|---------|---------|
| **High** | 85-100 | Strong evidence across sources | Multiple repos, consistent commits, certifications |
| **Medium** | 50-84 | Partial support or mixed signals | Good resume but sporadic GitHub |
| **Low** | 0-49 | Limited or weak evidence | Claims without visible support |

## 💡 Key Principles

1. **No Assumption of Dishonesty** - Missing evidence ≠ fraud
2. **Respect Constraints** - Enterprise work often proprietary
3. **Support Growth** - Focus on actionable improvements
4. **Celebrate Strengths** - Highlight well-supported skills
5. **Be Honest** - Acknowledge genuine gaps without accusation

## 🔍 What the Agent Analyzes

### From Resume
✓ Claimed skills, roles, projects  
✓ Work history and progression  
✓ Education and certifications  

### From GitHub
✓ Programming languages used  
✓ Repository count and quality  
✓ Commit frequency patterns  
✓ Project documentation  
✓ Code organization  

### From LeetCode
✓ Problem-solving ability  
✓ Algorithm knowledge  
✓ Difficulty level tackled  
✓ Practice consistency  

## 🎯 Use Cases

- **For Recruiters**: Understand skill alignment objectively
- **For Candidates**: Self-assess portfolio and identify improvements
- **For Career Coaches**: Provide specific development suggestions
- **For Platforms**: Enhance job matching and resume analysis

## ⚠️ Important Notes

### What It IS
✅ Decision support tool  
✅ Evidence alignment analysis  
✅ Portfolio assessment  
✅ Growth suggestion engine  

### What It Is NOT
❌ Hiring decision maker  
❌ Candidate ranking system  
❌ Fraud detector  
❌ Integrity verifier  

## 🛠️ Integration Points

Works with other agents:
- **ATS Analyzer** - Resume keyword matching
- **GitHub Analyzer** - Repository deep-dive
- **Interview Prep** - Use gaps for coaching

## 📝 Example Outputs

### Strong Evidence
```
confidence_level: "High"
authenticity_score: 88
strong_evidence:
  - "Python expertise: 25 repos, consistent commits, 50+ stars"
  - "FastAPI mastery: Production-grade APIs with excellent docs"
  - "Problem-solving: 187 LeetCode solutions"
risk_indicators:
  - "Could strengthen AWS expertise with Infrastructure-as-Code examples"
```

### Partial Evidence
```
confidence_level: "Medium"
authenticity_score: 58
strong_evidence:
  - "Data Science degree and relevant work history"
  - "Python skills demonstrated"
risk_indicators:
  - "Limited public ML projects despite claimed specialization"
  - "Sporadic GitHub activity (1-2 commits/month)"
improvement_suggestions:
  - "Build 1-2 public ML projects with detailed documentation"
  - "Share Kaggle competitions or Jupyter notebooks"
```

### No GitHub
```
confidence_level: "Medium"
authenticity_score: 72
strong_evidence:
  - "4+ years at enterprise companies"
  - "Relevant certifications (AWS, Kubernetes)"
  - "Senior-level responsibilities"
risk_indicators:
  - "Limited ability to assess hands-on coding without GitHub"
improvement_suggestions:
  - "Create GitHub profile with example projects"
  - "Build side projects showcasing microservices architecture"
  - "Share technical blog posts or architecture documentation"
```

## 🔗 Files Reference

- **Core Agent**: `app/core/authenticity_agent.py`
- **Schemas**: `app/models/authenticity.py`
- **Router**: `app/routers/authenticity.py`
- **Examples**: `app/core/authenticity_examples.py`
- **Tests**: `tests/test_authenticity_agent.py`
- **Documentation**: `AUTHENTICITY_AGENT_GUIDE.md`

## 🚨 Error Handling

If LLM fails, returns supportive fallback:
- Acknowledges data received
- Suggests providing more evidence (GitHub, LeetCode)
- Provides template for improvement

## 💬 Support

For questions or improvements:
1. Check the full guide: `AUTHENTICITY_AGENT_GUIDE.md`
2. Review examples: `app/core/authenticity_examples.py`
3. Run tests: `pytest tests/test_authenticity_agent.py`
4. Check error messages in response

## 🔐 Privacy & Ethics

✅ No data storage  
✅ No candidate profiling  
✅ No hiring decisions  
✅ Transparent reasoning  
✅ Respects career circumstances  
✅ Supportive-first approach  

---

**Remember**: This agent helps candidates strengthen their portfolio and understand skill alignment. It's a career coach, not a judge. 🎓
