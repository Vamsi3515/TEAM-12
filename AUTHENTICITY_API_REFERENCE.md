# 🔗 Authenticity Agent API Integration Reference

## Quick Start

### ✅ Correct Request Format

**Endpoint:** `POST http://localhost:8000/api/analyze-authenticity`

**Headers:**
```
Content-Type: application/json
```

**Body Structure:**
```json
{
  "resume": {
    "raw_text": "Your resume text here...",
    "skills": ["Python", "React"],
    "experience": [],
    "projects": [],
    "education": [],
    "certifications": []
  },
  "evidences": [
    {
      "type": "github_profile",
      "url": "https://github.com/username",
      "title": "GitHub Profile",
      "metadata": {}
    }
  ],
  "additional_context": "Optional context"
}
```

### ❌ Common Mistakes

**DON'T:** Use FormData
```javascript
// ❌ Wrong
const formData = new FormData();
formData.append('resume', file);
```

**DO:** Use JSON
```javascript
// ✅ Correct
const body = JSON.stringify({
  resume: { raw_text: "...", ... },
  evidences: [...]
});
```

**DON'T:** Send to wrong endpoint
```javascript
// ❌ Wrong
fetch('http://localhost:8000/api/authenticity/analyze', ...)
```

**DO:** Use correct endpoint
```javascript
// ✅ Correct
fetch('http://localhost:8000/api/analyze-authenticity', ...)
```

## Evidence Types

| Type | Description | Example |
|------|-------------|---------|
| `github_profile` | User's GitHub profile | `https://github.com/username` |
| `github_repo` | Specific repository | `https://github.com/user/repo` |
| `leetcode_profile` | LeetCode profile | `https://leetcode.com/username` |
| `certificate` | Certification link | Certificate URL |
| `portfolio` | Personal website | Portfolio URL |
| `blog` | Technical blog | Blog URL |
| `link` | Generic link | Any URL |

## Frontend Integration Code

```javascript
// Complete working example
const handleAnalyze = async () => {
  const evidences = [];
  
  // Add GitHub
  if (githubUrl) {
    evidences.push({
      type: 'github_profile',
      url: githubUrl,
      title: 'GitHub Profile',
      metadata: {}
    });
  }
  
  // Add LeetCode
  if (leetcodeUrl) {
    evidences.push({
      type: 'leetcode_profile',
      url: leetcodeUrl,
      title: 'LeetCode Profile',
      metadata: {}
    });
  }
  
  // Build request
  const requestBody = {
    resume: {
      raw_text: resumeText,
      skills: [],
      experience: [],
      projects: [],
      education: [],
      certifications: []
    },
    evidences: evidences
  };
  
  // Make request
  const response = await fetch('http://localhost:8000/api/analyze-authenticity', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });
  
  if (response.ok) {
    const data = await response.json();
    setResults(data);
  } else {
    const error = await response.json();
    console.error('API Error:', error);
  }
};
```

## Response Structure

```typescript
interface AuthenticityResponse {
  confidence_level: "High" | "Medium" | "Low";
  authenticity_score: number; // 0-100
  strong_evidence: string[];
  risk_indicators: string[];
  overall_assessment: string;
  improvement_suggestions: string[];
  skill_alignments: Array<{
    skill: string;
    confidence: "High" | "Medium" | "Low";
    evidence_source: string[];
    supporting_evidence: string[];
    gap_analysis: string | null;
  }>;
}
```

## Testing Commands

### Test Backend Directly
```bash
cd FastApi
python test_authenticity_integration.py
```

### Test with cURL
```bash
curl -X POST http://localhost:8000/api/analyze-authenticity \
  -H "Content-Type: application/json" \
  -d '{
    "resume": {
      "raw_text": "Software Engineer",
      "skills": [],
      "experience": [],
      "projects": [],
      "education": [],
      "certifications": []
    },
    "evidences": []
  }'
```

### Expected Response
```json
{
  "confidence_level": "Low",
  "authenticity_score": 35,
  "strong_evidence": [],
  "risk_indicators": [
    "No GitHub profile provided",
    "Limited verifiable evidence"
  ],
  "overall_assessment": "...",
  "improvement_suggestions": [
    "Add GitHub profile to showcase projects"
  ],
  "skill_alignments": []
}
```

## Error Handling

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "json_invalid",
      "msg": "JSON decode error"
    }
  ]
}
```
**Fix:** Check JSON syntax, ensure all required fields present

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```
**Fix:** Verify data types match schema

### CORS Error
```
Access to fetch blocked by CORS policy
```
**Fix:** Backend should have CORS enabled (already configured)

## Integration Checklist

- [ ] Backend running on port 8000
- [ ] Frontend using correct endpoint URL
- [ ] Sending JSON, not FormData
- [ ] Content-Type header set to application/json
- [ ] Request body matches AuthenticityExtendedInput schema
- [ ] Resume has at least raw_text field
- [ ] Evidences array properly formatted
- [ ] Error handling implemented
- [ ] Results properly displayed in UI

---

**Need Help?** Check [AUTHENTICITY_INTEGRATION_COMPLETE.md](AUTHENTICITY_INTEGRATION_COMPLETE.md) for detailed troubleshooting.
