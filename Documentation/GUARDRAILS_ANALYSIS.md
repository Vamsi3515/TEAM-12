# Guardrails Implementation Analysis

## What Are Guardrails in AI Engineering?

**Guardrails** are safety mechanisms and validation rules that constrain AI model outputs to ensure they are:

1. **Safe & Compliant** - Prevent harmful, unethical, or policy-violating responses
2. **Factually Accurate** - Check outputs against known data/sources
3. **Properly Formatted** - Validate structured responses (JSON, schemas)
4. **Within Scope** - Prevent off-topic or irrelevant responses
5. **Consistent** - Maintain business logic and constraints

### Common Guardrail Types:
- Output validators (JSON schema, regex patterns)
- Content filters (detecting toxic/harmful content)
- Fact-checking systems
- Token/length limits
- Prompt injection detection
- Request/response filtering
- Pydantic model validation

---

## Your 4 Agents & Guardrails Status

### ✅ Agent 1: Experience Authenticity Agent
**Status: WELL IMPLEMENTED**

**Guardrails Implemented:**

1. **System Prompt Constraints** (lines 23-36 in authenticity_agent.py)
   ```python
   - "You are SUPPORTIVE and CANDIDATE-FRIENDLY, NOT accusatory"
   - "You do NOT assume missing evidence means dishonesty"
   - "You do NOT penalize candidates for not having GitHub or LeetCode"
   - "You NEVER use words like fraud, fake, dishonest, false, deceptive"
   - Tone: "Encouraging, constructive, non-judgmental"
   ```

2. **Output Schema Validation** (Pydantic models)
   - Strict TypedDict models: `AuthenticityExtendedOutput`
   - Validates: confidence_level, authenticity_score (float), skill_alignments
   - Ensures all required fields present before return

3. **JSON Parsing Guards** (lines 244-280)
   ```python
   def _parse_json_response(response: str) -> Dict[str, Any]:
       - Handles empty responses (raises ValueError)
       - Tries direct JSON parse first
       - Falls back to regex extraction with markdown code blocks
       - Logs failures with response preview
       - Raises error if parsing fails (triggering fallback response)
   ```

4. **Fallback Mechanism** (lines 282-300)
   - `_fallback_response()` generates supportive default output if LLM fails
   - Prevents errors from exposing raw failures

5. **Score Boundary Constraints**
   - authenticity_score enforced as float type
   - Pydantic validation ensures type safety

6. **Test Coverage**
   - `test_no_accusatory_language()`: Verifies no forbidden terms in output
   - `test_json_response_parsing_*()`: Tests JSON parsing robustness
   - Checks for supportive tone enforcement

---

### ✅ Agent 2: Security Auditor Agent
**Status: WELL IMPLEMENTED**

**Guardrails Implemented:**

1. **Static Analysis Filters** (lines 43-90)
   ```python
   - SQL injection pattern detection (regex-based)
   - Hardcoded secret detection (API_KEY, TOKEN, PASSWORD patterns)
   - Returns violations as structured dicts with severity levels
   - Deduplicates findings before returning
   ```

2. **AI-Enhanced Verification** (lines 157-226)
   ```python
   - LLM validates static findings: "Verify static findings are REAL vulnerabilities"
   - Eliminates false positives through AI inspection
   - Temperature=0.1 (very low) for deterministic analysis
   ```

3. **JSON Output Validation** (lines 248-268)
   ```python
   - Try/except wrapping for JSON parsing
   - Fallback repair mechanism: calls LLM to fix malformed JSON
   - Graceful degradation: uses static results if AI fails
   - Validates required fields: vulnerabilities, risk_score, summary
   ```

4. **Risk Scoring Constraints** (lines 292-293)
   ```python
   - risk_score = max(0.0, 100.0 - (total_risk_points * 0.8))
   - Score bounded: [0.0, 100.0] using max() function
   - Severity weights: critical=25, high=15, medium=8, low=3
   ```

5. **Severity Enumeration**
   - Only allows: "critical", "high", "medium", "low"
   - Validates in LLM prompt requirements
   - Deduplicates vulnerabilities by issue name

6. **Code Length Bounds**
   ```python
   - Truncates code to first 5000 chars
   - Shows message: "... ({remaining} more characters)"
   - Prevents token overflow
   ```

---

### ✅ Agent 3: ATS Analyzer Agent
**Status: WELL IMPLEMENTED**

**Guardrails Implemented:**

1. **Prompt Template Constraints** (lines 41-65)
   ```python
   - Requires specific JSON schema in output
   - Rules: 
     * "Use concise bullets (max 3 items per list)"
     * "Keep each string ≤ 140 characters"
     * "Keep entire JSON under ~400 tokens"
     * "Return compact JSON only (no markdown/code fences)"
   ```

2. **Text Truncation Guards** (lines 121-127)
   ```python
   def _truncate(text: str, limit: int) -> str:
       - Truncates long text to keep prompt size bounded
       - Preserves up to specified limit + "..."
   ```

3. **JSON Repair Mechanism** (lines 130-155)
   ```python
   def _repair_json(text: str) -> Optional[dict]:
       - Closes unclosed JSON braces/brackets
       - Handles truncated responses
       - Returns None if repair fails (graceful degradation)
   ```

4. **Code Fence Stripping** (lines 101-119)
   ```python
   def _strip_code_fences(text: str) -> str:
       - Removes markdown ```json or ``` markers
       - Handles leading "json" keyword
       - Returns clean JSON content
   ```

5. **Output Schema Validation**
   - Pydantic model: `ATSAnalyzeOutput`
   - Enforces: ats_score (int), rejection_reasons, strengths, issues, suggestions, summary
   - Validates sent_to_email boolean

6. **Max Tokens Constraint**
   ```python
   - call_chat(..., max_tokens=800)
   - Prevents runaway token usage
   ```

---

### ✅ Agent 4: GitHub Analyzer Agent
**Status: PARTIALLY IMPLEMENTED**

**Guardrails Implemented:**

1. **Input URL Validation** (lines 15-36)
   ```python
   def parse_owner_repo(repo_url: str):
       - Normalizes various GitHub URL formats
       - Handles: https://, git://, git@, owner/repo formats
       - Validates minimum 2 parts (owner/repo)
       - Raises ValueError with clear message if invalid
   ```

2. **HTTP Error Handling** (lines 58-70)
   ```python
   - Checks for 403 (rate limit/private repo) with specific guidance
   - Catches HTTPStatusError and RequestError separately
   - Provides helpful error messages (mentions GITHUB_TOKEN)
   - Validates response.is_success for additional API calls
   ```

3. **Rate Limiting Protection**
   - Respects GitHub API rate limits
   - Suggests authentication: "Set GITHUB_TOKEN/GITHUB_PAT for authenticated requests"
   - Timeout: 30 seconds (lines 53)

4. **Output Schema Validation**
   ```python
   class GitHubAnalyzeOutput(BaseModel):
       - tech_stack: List[str]
       - metrics: List[GitHubMetric]
       - strengths, weaknesses, suggestions: List[str]
       - evidence_ids: List[str]
   ```

5. **Graceful Degradation**
   ```python
   - README fetch wrapped in try/except (lines 85-87)
   - Languages fetch wrapped in try/except (lines 89-92)
   - Commits fetch has try/except (lines 94+)
   - Missing data doesn't crash analysis
   ```

**⚠️ Gaps in GitHub Agent:**
- No output bounds validation (metrics could be unbounded)
- No response size limits
- No content filtering on repository descriptions
- No PII detection (could expose private repo details)

---

## Summary Table: Guardrails Across Agents

| Guardrail Type | Authenticity | Security | ATS | GitHub |
|---|---|---|---|---|
| **System Prompt Constraints** | ✅ Excellent | ✅ Yes | ✅ Yes | ⚠️ Minimal |
| **Output Schema Validation** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **JSON Parsing Guards** | ✅ Robust | ✅ Repair+Fallback | ✅ Repair | ⚠️ Basic |
| **Boundary Constraints** | ✅ Yes | ✅ Score/Severity | ✅ Tokens/Length | ⚠️ No |
| **Input Validation** | ⚠️ Minimal | ✅ Yes | ⚠️ Basic | ✅ Good |
| **Error Handling** | ✅ Try/Except+Fallback | ✅ Cascading | ✅ Try/Except | ✅ Yes |
| **Content Filtering** | ✅ Tone Guards | ✅ Yes | ⚠️ No | ⚠️ No |
| **Rate Limiting** | N/A | N/A | N/A | ✅ Yes |
| **Test Coverage** | ✅ Dedicated Tests | ⚠️ Basic | ⚠️ Minimal | ⚠️ Minimal |

---

## Recommendations

### For Authenticity Agent (Strong):
- ✅ Keep current implementation
- Consider adding: Max length validation for evidence items

### For Security Agent (Strong):
- ✅ Keep current implementation
- Consider adding: CWE mapping validation, CVSS score bounds

### For ATS Agent (Strong):
- ✅ Keep current implementation
- Consider adding: Rejection reason validation (no generic responses)

### For GitHub Agent (Needs Enhancement):
1. **Add Output Bounds**
   ```python
   # Limit metrics to max 10 items
   metrics = metrics[:10]
   ```

2. **Add Response Size Validation**
   ```python
   if len(repo_data) > 10000:  # bytes
       repo_data = truncate_large_fields(repo_data)
   ```

3. **Add PII Detection** (for private repo descriptions)
   ```python
   # Filter sensitive patterns from descriptions
   description = filter_pii(description)
   ```

4. **Add Content Filtering**
   ```python
   forbidden_keywords = ["credit card", "password", "secret"]
   if any(kw in description.lower() for kw in forbidden_keywords):
       description = "[Content filtered]"
   ```

---

## Conclusion

**All 4 agents have guardrails implemented**, with:
- **Tier 1 (Excellent):** Authenticity, Security, ATS agents
- **Tier 2 (Good):** GitHub agent (functional but could be enhanced)

The system uses **defense-in-depth**:
1. Input validation
2. System prompt constraints
3. Output schema validation
4. Error handling + fallback mechanisms
5. Boundary constraints (scores, token limits)

This is a **production-ready** implementation with appropriate safeguards for an AI engineering project.
