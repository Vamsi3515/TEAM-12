import json
import re
from typing import Any, Dict, List
from app.core.embeddings import embed
from app.core.vectorstore import get_or_create_collection
from app.core.llm_client import call_chat
from app.core.security_rag_data import security_knowledge
import time

SECURITY_LOG: List[Dict[str, Any]] = []


# -------------------------------------------------------------------
# 1. Seed RAG
# -------------------------------------------------------------------
def seed_security_collection(name="security_knowledge"):
    col = get_or_create_collection(name)
    try:
        if col.count() == 0:
            texts = [x["text"] for x in security_knowledge]
            ids = [x["id"] for x in security_knowledge]
            emb = embed(texts)
            col.add(documents=texts, ids=ids, embeddings=emb)
    except:
        texts = [x["text"] for x in security_knowledge]
        ids = [x["id"] for x in security_knowledge]
        emb = embed(texts)
        col.add(documents=texts, ids=ids, embeddings=emb)
    return col


# -------------------------------------------------------------------
# 2. RAG Retrieval
# -------------------------------------------------------------------
def retrieve_security_docs(collection, code: str, k=3):
    q_emb = embed([code])[0]
    res = collection.query(query_embeddings=[q_emb], n_results=k)
    
    docs = res["documents"][0] if "documents" in res else []
    ids = res["ids"][0] if "ids" in res else []

    retrievals = []
    for i, d in enumerate(docs):
        retrievals.append({"id": ids[i], "text": d})

    SECURITY_LOG.append({"input": code[:200], "results": retrievals, "time": time.time()})
    return retrievals


# -------------------------------------------------------------------
# 3. Static Rule-Based Vulnerability Detection
# -------------------------------------------------------------------
def run_static_analysis(code: str):
    vulnerabilities = []
    lines = code.split("\n")

    # ---- SQL Injection (more precise pattern) ----
    sql_injection_patterns = [
        r'execute\s*\(\s*f["\'].*?(SELECT|INSERT|UPDATE|DELETE)',
        r'execute\s*\(\s*["\'].*?\{.*?(SELECT|INSERT|UPDATE|DELETE)',
        r'(SELECT|INSERT|UPDATE|DELETE).*?\+.*?',
    ]
    
    for pattern in sql_injection_patterns:
        if re.search(pattern, code, re.IGNORECASE | re.DOTALL):
            matching_lines = [i+1 for i, line in enumerate(lines) if re.search(pattern, line, re.IGNORECASE)]
            if matching_lines:
                vulnerabilities.append({
                    "issue": "SQL Injection",
                    "severity": "critical",
                    "explanation": "Dynamic SQL query with string concatenation detected.",
                    "line_numbers": matching_lines[:5],
                    "fix_suggestion": "Use prepared statements or parameterized queries."
                })
                break

    # ---- Hardcoded secret ----
    secret_patterns = [
        r'(API_KEY|TOKEN|PASSWORD|SECRET)\s*=\s*["\'][^"\'\n]{10,}["\']',
        r'(api_key|token|password|secret)\s*:\s*["\'][^"\'\n]{10,}["\']',
    ]
    
    for pattern in secret_patterns:
        matches = list(re.finditer(pattern, code, re.IGNORECASE))
        if matches:
            matching_lines = []
            for match in matches[:3]:
                line_num = code[:match.start()].count('\n') + 1
                matching_lines.append(line_num)
            
            if matching_lines:
                vulnerabilities.append({
                    "issue": "Hardcoded Secret",
                    "severity": "high",
                    "explanation": "Hardcoded credentials found in source code.",
                    "line_numbers": matching_lines,
                    "fix_suggestion": "Use environment variables or secret managers."
                })
                break

    # ---- Dangerous eval() ----
    if re.search(r'\beval\s*\(', code):
        matching_lines = [i+1 for i, line in enumerate(lines) if re.search(r'\beval\s*\(', line)]
        if matching_lines:
            vulnerabilities.append({
                "issue": "Arbitrary Code Execution (eval)",
                "severity": "critical",
                "explanation": "Use of eval() allows arbitrary code execution.",
                "line_numbers": matching_lines[:3],
                "fix_suggestion": "Avoid eval(). Use JSON.parse or safe parsing libraries."
            })

    # ---- Command Injection ----
    if re.search(r'child_process\.exec\s*\(', code):
        matching_lines = [i+1 for i, line in enumerate(lines) if 'child_process.exec' in line]
        if matching_lines:
            vulnerabilities.append({
                "issue": "Command Injection (exec)",
                "severity": "critical",
                "explanation": "child_process.exec can allow remote command execution.",
                "line_numbers": matching_lines[:3],
                "fix_suggestion": "Use execFile or safe command execution."
            })

    if re.search(r'\bos\.system\s*\(', code):
        matching_lines = [i+1 for i, line in enumerate(lines) if re.search(r'\bos\.system\s*\(', line)]
        if matching_lines:
            vulnerabilities.append({
                "issue": "Command Injection (os.system)",
                "severity": "high",
                "explanation": "os.system() executes shell commands unsafely.",
                "line_numbers": matching_lines[:3],
                "fix_suggestion": "Use subprocess.run with argument lists."
            })

    return vulnerabilities


# -------------------------------------------------------------------
# 4. Hybrid AI Security Analysis
# -------------------------------------------------------------------
async def analyze_code_security(code: str, language: str = "auto"):
    
    print(f"\n[Security Analysis] Analyzing {len(code)} characters of code")
    print(f"[Security Analysis] First 200 chars: {code[:200]}...")

    # --- STATIC ANALYSIS FIRST (guaranteed vulnerabilities detection) ---
    static_vulns = run_static_analysis(code)
    print(f"[Security Analysis] Found {len(static_vulns)} static vulnerabilities")

    # --- Seed + retrieve RAG ---
    col = seed_security_collection()
    rag_docs = retrieve_security_docs(col, code, k=3)
    rag_context = "\n\n".join([f"ID:{r['id']}\n{r['text']}" for r in rag_docs])

    # --- LLM-enhanced vulnerability analysis with deep investigation ---
    ai_prompt = f"""You are an Expert Application Security Auditor performing a comprehensive security review.

=== CODE UNDER ANALYSIS ===
Language: {language}
Total Length: {len(code)} characters
Files Analyzed: Multiple source files from repository

Code Content:
```
{code[:5000]}
```
{f"... ({len(code) - 5000} more characters)" if len(code) > 5000 else ""}

=== STATIC ANALYSIS RESULTS ===
{json.dumps(static_vulns, indent=2) if static_vulns else "No static vulnerabilities detected"}

=== SECURITY KNOWLEDGE BASE (RAG) ===
{rag_context}

=== YOUR TASK: DEEP SECURITY INVESTIGATION ===

Perform a thorough, line-by-line security audit. Investigate:

1. **INJECTION VULNERABILITIES**
   - SQL Injection: Check for dynamic query construction, string concatenation with SQL
   - Command Injection: Look for os.system(), subprocess without shell=False, exec()
   - Code Injection: Identify eval(), exec(), compile() with user input
   - XSS: Check for unescaped output in templates, innerHTML usage
   - LDAP/XML/Template Injection: Identify unsafe parsers

2. **AUTHENTICATION & ACCESS CONTROL**
   - Hardcoded credentials, API keys, tokens
   - Weak password policies, missing authentication
   - Broken access control, IDOR vulnerabilities
   - Session management issues, missing CSRF protection

3. **CRYPTOGRAPHIC FAILURES**
   - Use of weak algorithms (MD5, SHA1 for passwords)
   - Hardcoded encryption keys
   - Missing TLS/SSL, insecure random number generation
   - Plain text storage of sensitive data

4. **CONFIGURATION & DEPLOYMENT**
   - Debug mode enabled in production
   - Verbose error messages exposing internals
   - Missing security headers
   - Default credentials or configurations

5. **DATA EXPOSURE & VALIDATION**
   - Sensitive data in logs or error messages
   - Missing input validation
   - Path traversal vulnerabilities
   - Unsafe deserialization

6. **DEPENDENCY & THIRD-PARTY RISKS**
   - Outdated or vulnerable libraries
   - Unsafe file uploads
   - XXE vulnerabilities in XML parsers

=== ANALYSIS REQUIREMENTS ===
- Verify static findings are REAL vulnerabilities (eliminate false positives)
- Find NEW vulnerabilities not caught by static analysis
- Provide SPECIFIC line numbers where issues exist
- Rate severity accurately: low/medium/high/critical
- Give actionable remediation steps
- Calculate overall risk_score (0-100) based on:
  * Number of vulnerabilities
  * Severity weights: critical=25, high=15, medium=8, low=3
  * Max score capped at 100

=== OUTPUT FORMAT ===
Return ONLY valid JSON (no markdown, no explanations outside JSON):
{{
  "vulnerabilities": [
    {{
      "issue": "Specific vulnerability name",
      "severity": "critical|high|medium|low",
      "explanation": "Detailed explanation of the security risk",
      "line_numbers": [actual line numbers from code],
      "fix_suggestion": "Step-by-step remediation guidance"
    }}
  ],
  "risk_score": 0-100,
  "summary": "Brief overall assessment of code security posture",
  "evidence_ids": ["{rag_docs[0]['id'] if rag_docs else ''}", "{rag_docs[1]['id'] if len(rag_docs) > 1 else ''}", "{rag_docs[2]['id'] if len(rag_docs) > 2 else ''}"]
}}

CRITICAL: Only report vulnerabilities that ACTUALLY EXIST in the provided code. Do not make assumptions."""

    raw = await call_chat(ai_prompt, temperature=0.1, max_tokens=1500)

    # Fix JSON if needed
    try:
        parsed = json.loads(raw)
    except:
        print(f"[Security Analysis] JSON parse failed, attempting fix...")
        fix_prompt = f"Convert the following to strict valid JSON (no markdown):\n{raw}"
        fixed = await call_chat(fix_prompt, temperature=0.1, max_tokens=1200)
        try:
            parsed = json.loads(fixed)
        except:
            print(f"[Security Analysis] JSON fix failed, using static results only")
            parsed = {
                "vulnerabilities": static_vulns,
                "risk_score": sum(25 if v["severity"]=="critical" else 15 if v["severity"]=="high" else 8 for v in static_vulns),
                "summary": "Analysis completed with static findings only.",
                "evidence_ids": [r["id"] for r in rag_docs]
            }


    # --- Merge static + AI vulnerabilities (deduplicate by issue name) ---
    ai_vulns = parsed.get("vulnerabilities", [])
    all_vulns = static_vulns.copy()
    static_issue_names = {v.get("issue", "").lower() for v in static_vulns}

    # Add AI findings without duplicates (based on issue name)
    for v in ai_vulns:
        issue_name = v.get("issue", "").lower()
        if issue_name not in static_issue_names:
            all_vulns.append(v)
            static_issue_names.add(issue_name)
    
    print(f"[Security Analysis] Total vulnerabilities after merge: {len(all_vulns)}")

    # Calculate security score (0-100, higher is better)
    # Risk points: critical=25, high=15, medium=8, low=3
    severity_points = {"critical": 25, "high": 15, "medium": 8, "low": 3}
    total_risk_points = sum(severity_points.get(v.get("severity","low").lower(), 3) for v in all_vulns)
    
    # Convert risk points to security score (inverse)
    # 0 vulns = 100 score, more vulns = lower score
    if total_risk_points == 0:
        security_score = 100.0
    else:
        # Security score decreases as risk increases
        # Max reasonable risk = 150 points (e.g., 6 critical vulns)
        security_score = max(0.0, 100.0 - (total_risk_points * 0.8))
    
    # Calculate risk level
    if security_score >= 80:
        risk_level = "low"
    elif security_score >= 60:
        risk_level = "medium"
    elif security_score >= 40:
        risk_level = "high"
    else:
        risk_level = "critical"
    
    print(f"[Security Analysis] Security Score: {security_score:.1f}/100 ({risk_level} risk)")

    return {
        "vulnerabilities": all_vulns,
        "security_score": round(security_score, 1),
        "risk_score": round(total_risk_points, 1),  # Keep for backwards compatibility
        "risk_level": risk_level,
        "summary": parsed.get("summary", "Security analysis completed."),
        "evidence_ids": [r["id"] for r in rag_docs],
        "evidence_snippets": [
            {"id": r["id"], "snippet": r["text"][:300]} for r in rag_docs
        ]
    }