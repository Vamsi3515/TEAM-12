# Integration Guide: Experience Authenticity Agent with Existing Analyzers

## 🔗 Overview

This guide explains how to integrate the **Experience Authenticity & Skill Consistency Agent** with your existing **ATS Analyzer** and **GitHub Analyzer** to create a comprehensive employability assessment platform.

---

## 📌 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input                               │
│          (Resume Text + GitHub URL + LeetCode ID)           │
└─────────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┬──────────────────┐
        ↓                  ↓                  ↓
   ┌─────────┐      ┌────────────┐    ┌─────────┐
   │ Resume  │      │   GitHub   │    │LeetCode │
   │ Parser  │      │  Analyzer  │    │ Scraper │
   └────┬────┘      └─────┬──────┘    └────┬────┘
        │                 │                 │
        ├─ ResumeData ────┤                 │
        ├─ GitHubEvidence │                 │
        └─ LeetCodeEvidence────────────────┘
                           ↓
        ┌──────────────────────────────────────┐
        │ Authenticity & Skill Consistency     │
        │          Agent                       │
        └──────────────────┬───────────────────┘
                           ↓
             ┌──────────────────────────┐
             │ AuthenticityAnalysis     │
             │ (Confidence + Evidence)  │
             └──────────────────────────┘
                           ↓
        ┌──────────────────────────────────────┐
        │      Frontend Dashboard              │
        │  (Visualize alignment & suggestions) │
        └──────────────────────────────────────┘
```

---

## 🔄 Integration Points

### 1. **Resume Parser → Authenticity Agent**

Your existing resume parser extracts structured data:

```python
# From your resume parser
resume_data = {
    "full_name": "Alice Johnson",
    "skills": ["Python", "FastAPI", "React"],
    "experience": [...],
    "projects": [...]
}

# Convert to AuthenticityAnalysisInput
from app.models.authenticity import ResumeData, AuthenticityAnalysisInput

resume = ResumeData(**resume_data)
```

### 2. **GitHub Analyzer → Authenticity Agent**

Your existing GitHub analyzer already fetches profile data:

```python
# From your GitHub analyzer (github_agent.py)
github_data = {
    "username": "alice-dev",
    "languages": ["Python", "JavaScript"],
    "repo_count": 25,
    "commit_frequency": "consistent",
    "top_projects": [...],
    "readme_quality": "excellent"
}

# Convert to GitHubEvidence
from app.models.authenticity import GitHubEvidence

github = GitHubEvidence(**github_data)
```

### 3. **Optional: LeetCode Integration**

If you want to include LeetCode metrics:

```python
# From LeetCode scraper (create new or use existing)
leetcode_data = {
    "problems_solved": 187,
    "difficulty_distribution": {"Easy": 65, "Medium": 89, "Hard": 33},
    "recent_activity": True
}

from app.models.authenticity import LeetCodeEvidence

leetcode = LeetCodeEvidence(**leetcode_data)
```

---

## 🛠️ Implementation Patterns

### Pattern 1: Sequential Analysis
Analyze resume → GitHub → then run authenticity check

```python
async def analyze_candidate_full(resume_text: str, github_url: str):
    """Full candidate analysis pipeline."""
    
    # Step 1: Parse resume
    from app.routers.resume_extractor import parse_resume_async
    resume_data = await parse_resume_async(resume_text)
    resume = ResumeData(**resume_data)
    
    # Step 2: Analyze GitHub
    from app.core.github_agent import analyze_github_repo
    github_data = await analyze_github_repo(github_url)
    github = GitHubEvidence(**github_data)
    
    # Step 3: Check authenticity
    from app.core.authenticity_agent import analyze_authenticity
    from app.models.authenticity import AuthenticityAnalysisInput
    
    input_data = AuthenticityAnalysisInput(
        resume=resume,
        github=github
    )
    
    authenticity_result = await analyze_authenticity(input_data)
    
    return authenticity_result
```

### Pattern 2: Parallel Analysis
Run resume + GitHub analysis in parallel, then combine

```python
import asyncio

async def analyze_candidate_parallel(resume_text: str, github_url: str):
    """Faster analysis with parallel fetching."""
    
    # Run both analyses in parallel
    resume_task = parse_resume_async(resume_text)
    github_task = analyze_github_repo(github_url)
    
    resume_data, github_data = await asyncio.gather(
        resume_task,
        github_task
    )
    
    # Then run authenticity analysis
    resume = ResumeData(**resume_data)
    github = GitHubEvidence(**github_data)
    
    input_data = AuthenticityAnalysisInput(resume=resume, github=github)
    return await analyze_authenticity(input_data)
```

### Pattern 3: Conditional Analysis
Only run authenticity check if GitHub is available

```python
async def analyze_with_optional_github(resume_text: str, github_url: Optional[str] = None):
    """Run authenticity check with or without GitHub."""
    
    resume_data = await parse_resume_async(resume_text)
    resume = ResumeData(**resume_data)
    
    github = None
    if github_url:
        try:
            github_data = await analyze_github_repo(github_url)
            github = GitHubEvidence(**github_data)
        except Exception as e:
            print(f"GitHub analysis failed: {e}")
            # Continue without GitHub - authenticity agent handles this
    
    input_data = AuthenticityAnalysisInput(
        resume=resume,
        github=github,
        additional_context="No GitHub provided" if not github else None
    )
    
    return await analyze_authenticity(input_data)
```

---

## 🎯 Enhanced Endpoint Example

Create a comprehensive analysis endpoint that combines all three agents:

```python
# Add to app/routers/authenticity.py or create new file

from fastapi import APIRouter, HTTPException
from app.models.authenticity import AuthenticityAnalysisInput, AuthenticityAnalysisOutput
from app.models.ats import ATSAnalyzeOutput
from app.models.schemas import GitHubAnalyzeOutput
from pydantic import BaseModel
from typing import Optional

class ComprehensiveAnalysisInput(BaseModel):
    resume_text: str
    github_url: Optional[str] = None
    job_description: Optional[str] = None

class ComprehensiveAnalysisOutput(BaseModel):
    ats_analysis: ATSAnalyzeOutput
    github_analysis: GitHubAnalyzeOutput
    authenticity_analysis: AuthenticityAnalysisOutput
    combined_insights: str  # Summary combining all three

router = APIRouter(tags=["Comprehensive Analysis"])

@router.post("/analyze-comprehensive")
async def analyze_comprehensive(input_data: ComprehensiveAnalysisInput) -> ComprehensiveAnalysisOutput:
    """
    Comprehensive candidate analysis combining:
    - ATS Score (resume matching)
    - GitHub Profile (coding ability)
    - Authenticity Score (skill alignment)
    """
    
    # Run all three analyses
    from app.core.ats_agent import analyze_ats
    from app.core.github_agent import analyze_github_repo
    from app.core.authenticity_agent import analyze_authenticity
    from app.routers.resume_extractor import parse_resume_async
    
    import asyncio
    
    # Parse resume
    resume_data = await parse_resume_async(input_data.resume_text)
    
    # Run ATS analysis
    ats_result = await analyze_ats(
        resume_text=input_data.resume_text,
        job_description=input_data.job_description
    )
    
    github_result = None
    authenticity_result = None
    
    if input_data.github_url:
        try:
            # Run GitHub analysis
            github_result = await analyze_github_repo(input_data.github_url)
            
            # Run authenticity analysis
            from app.models.authenticity import ResumeData, GitHubEvidence, AuthenticityAnalysisInput
            
            resume = ResumeData(**resume_data)
            github = GitHubEvidence(**github_result.model_dump())
            
            authenticity_result = await analyze_authenticity(
                AuthenticityAnalysisInput(resume=resume, github=github)
            )
        except Exception as e:
            print(f"GitHub/Authenticity analysis error: {e}")
    
    # Generate combined insights
    combined_insights = generate_combined_insights(
        ats_result,
        github_result,
        authenticity_result
    )
    
    return ComprehensiveAnalysisOutput(
        ats_analysis=ats_result,
        github_analysis=github_result,
        authenticity_analysis=authenticity_result,
        combined_insights=combined_insights
    )

def generate_combined_insights(ats, github, authenticity) -> str:
    """Combine insights from all three analyzers."""
    insights = []
    
    if ats:
        insights.append(f"Resume Score: {ats.ats_score}% - {ats.summary}")
    
    if github:
        insights.append(f"GitHub Tech Stack: {', '.join(github.tech_stack)}")
    
    if authenticity:
        insights.append(f"Skill Alignment: {authenticity.confidence_level} - {authenticity.overall_assessment}")
    
    return "\n".join(insights)
```

---

## 📊 Frontend Integration

### Display Components

```javascript
// Frontend - React component example

function CandidateAnalysis({ resumeText, githubUrl }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    setLoading(true);
    try {
      // Call comprehensive endpoint
      const response = await fetch('/api/analyze-comprehensive', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          github_url: githubUrl
        })
      });
      
      const data = await response.json();
      setAnalysis(data);
    } finally {
      setLoading(false);
    }
  }

  if (!analysis) return <button onClick={handleAnalyze}>Analyze</button>;

  return (
    <div>
      {/* ATS Score */}
      <section>
        <h3>Resume Quality</h3>
        <div>Score: {analysis.ats_analysis.ats_score}%</div>
      </section>

      {/* GitHub Analysis */}
      {analysis.github_analysis && (
        <section>
          <h3>Coding Profile</h3>
          <p>Tech Stack: {analysis.github_analysis.tech_stack.join(', ')}</p>
        </section>
      )}

      {/* Authenticity Analysis */}
      {analysis.authenticity_analysis && (
        <section>
          <h3>Skill Alignment</h3>
          <div>
            <p>Confidence: <strong>{analysis.authenticity_analysis.confidence_level}</strong></p>
            <p>Score: {analysis.authenticity_analysis.authenticity_score}/100</p>
            
            <h4>Strengths</h4>
            <ul>
              {analysis.authenticity_analysis.strong_evidence.map(s => (
                <li key={s}>{s}</li>
              ))}
            </ul>
            
            <h4>Areas to Improve</h4>
            <ul>
              {analysis.authenticity_analysis.improvement_suggestions.map(s => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* Combined Insights */}
      <section>
        <h3>Overall Assessment</h3>
        <p>{analysis.combined_insights}</p>
      </section>
    </div>
  );
}
```

---

## 📋 Data Transformation Examples

### From GitHub Analyzer to Authenticity

```python
# Your GitHub analyzer returns this structure
github_analysis = {
    "tech_stack": ["Python", "FastAPI", "React"],
    "metrics": [...],
    "repo_summary": "..."
}

# Transform to GitHubEvidence for authenticity agent
github_evidence = GitHubEvidence(
    languages=github_analysis["tech_stack"],
    repo_count=25,  # Extract from your analysis
    readme_quality="excellent",  # Extract from metrics
    contribution_pattern="consistent"  # Extract from metrics
)
```

### From ATS Analyzer to Authenticity

```python
# Your ATS analyzer extracts resume
ats_input = {
    "resume_text": "..."
}

# Parse it for authenticity agent
from app.routers.resume_extractor import parse_resume

resume_data = parse_resume(ats_input["resume_text"])
resume = ResumeData(**resume_data)
```

---

## 🧪 Testing the Integration

### Test Script

```python
# tests/test_integration.py

import pytest
import asyncio
from app.models.authenticity import (
    ResumeData, GitHubEvidence, AuthenticityAnalysisInput
)
from app.core.authenticity_agent import analyze_authenticity

@pytest.mark.asyncio
async def test_authenticity_with_github():
    """Test authenticity agent with GitHub data."""
    
    resume = ResumeData(
        skills=["Python", "FastAPI"],
        experience=[{"title": "Engineer", "company": "Corp"}]
    )
    
    github = GitHubEvidence(
        languages=["Python"],
        repo_count=10,
        contribution_pattern="consistent"
    )
    
    result = await analyze_authenticity(
        AuthenticityAnalysisInput(resume=resume, github=github)
    )
    
    assert result.confidence_level in ["High", "Medium", "Low"]
    assert 0 <= result.authenticity_score <= 100

@pytest.mark.asyncio
async def test_authenticity_without_github():
    """Test authenticity agent without GitHub."""
    
    resume = ResumeData(
        skills=["Java", "Spring"],
        experience=[{"title": "Senior Engineer", "company": "BigTech"}]
    )
    
    result = await analyze_authenticity(
        AuthenticityAnalysisInput(resume=resume)
    )
    
    # Should handle gracefully without GitHub
    assert result.confidence_level in ["High", "Medium", "Low"]
```

---

## 📈 Performance Considerations

### Caching
Consider caching GitHub analysis results:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
async def cached_github_analysis(repo_url: str):
    """Cache GitHub analysis for 1 hour."""
    return await analyze_github_repo(repo_url)
```

### Rate Limiting
GitHub API has rate limits:

```python
import aioredis

redis = aioredis.from_url("redis://localhost")

async def check_rate_limit(user_id: str) -> bool:
    """Check if user exceeded rate limit."""
    key = f"auth_analysis:{user_id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 3600)  # 1 hour
    return count <= 10  # Max 10 per hour
```

---

## 🔒 Security Considerations

### Input Validation

```python
from pydantic import validator

class AuthenticityRequest(BaseModel):
    resume_text: str
    github_url: Optional[str] = None
    
    @validator('github_url')
    def validate_github_url(cls, v):
        if v and not v.startswith('https://github.com/'):
            raise ValueError('Invalid GitHub URL')
        return v
```

### Access Control

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    # Implement your auth logic
    return credentials
```

---

## 📞 Troubleshooting

### Issue: GitHub analysis fails
```python
# Handle gracefully
try:
    github_data = await analyze_github_repo(url)
except Exception as e:
    print(f"GitHub error: {e}")
    github_data = None  # Continue without GitHub
```

### Issue: Resume parsing incomplete
```python
# Provide additional context
input_data = AuthenticityAnalysisInput(
    resume=resume,
    github=github,
    additional_context="Candidate has 10+ years at top companies, limited public portfolio due to proprietary work"
)
```

### Issue: LLM timeouts
```python
# Implement retry logic
async def analyze_with_retry(input_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await analyze_authenticity(input_data)
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

---

## 🎓 Best Practices

1. **Always provide context** - Include job description or role context if available
2. **Handle missing data gracefully** - GitHub/LeetCode optional, not required
3. **Cache external API calls** - GitHub API has rate limits
4. **Show confidence levels** - Don't hide uncertainty from users
5. **Provide actionable feedback** - Suggest specific next steps
6. **Respect privacy** - Don't require public portfolios
7. **Update regularly** - Refresh GitHub data on demand, cache for 1 hour

---

## ✅ Integration Checklist

- [ ] Install/import authenticity agent modules
- [ ] Add schema imports to your data layer
- [ ] Create authenticity router in your API
- [ ] Register router in main.py
- [ ] Implement data transformation from existing analyzers
- [ ] Test with example candidates
- [ ] Deploy and monitor
- [ ] Collect feedback
- [ ] Iterate on prompts/scoring

---

**Ready to integrate?** Start with [Pattern 1](#pattern-1-sequential-analysis) above and adapt to your architecture.
