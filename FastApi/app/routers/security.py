"""Security Auditor API Router - OWASP vulnerability detection endpoint."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import SecurityAuditInput, SecurityAuditOutput
from app.core.security_agent import analyze_code_security
from app.core.github_agent import fetch_github_repo
import base64

router = APIRouter(prefix="/api/security", tags=["Security Auditor"])


@router.post("/analyze", response_model=SecurityAuditOutput)
async def analyze_code(request: SecurityAuditInput):
    """
    Analyze source code for OWASP vulnerabilities using hybrid analysis:
    - Static pattern matching for known vulnerability signatures
    - AI-powered LLM analysis with RAG for context-aware detection
    
    **Supports:**
    - Direct code snippets
    - GitHub repository URLs
    
    **Features:**
    - Detects SQL Injection, XSS, IDOR, Command Injection, etc.
    - OWASP Top 10 coverage
    - CWE mapping
    - Severity scoring
    - Remediation guidance
    
    **Example Request (Code):**
    ```json
    {
        "code": "cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
        "inputType": "code"
    }
    ```
    
    **Example Request (GitHub):**
    ```json
    {
        "repoUrl": "https://github.com/owner/repo",
        "inputType": "repo"
    }
    ```
    
    **Returns:**
    - Security score (0-100)
    - Risk level (low/medium/high/critical)
    - Detailed vulnerability list with:
        - Severity and category
        - Line numbers
        - CWE and OWASP mappings
        - Remediation steps
    - RAG evidence used for analysis
    """
    
    try:
        code_to_analyze = ""
        
        # Handle GitHub URL input
        if request.inputType == "repo":
            if not request.repoUrl or not request.repoUrl.strip():
                raise HTTPException(
                    status_code=400,
                    detail="GitHub repository URL cannot be empty"
                )
            
            # Parse owner and repo from URL
            from app.core.github_agent import parse_owner_repo
            import os
            import httpx
            
            try:
                owner, repo = parse_owner_repo(request.repoUrl)
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc))
            
            # Fetch actual source code files from repository
            github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT")
            headers = {
                "Accept": "application/vnd.github+json",
                "User-Agent": "fastapi/1.0",
            }
            if github_token:
                headers["Authorization"] = f"Bearer {github_token}"
            
            code_parts = []
            default_branch = "main"
            
            async with httpx.AsyncClient(timeout=30, headers=headers) as client:
                # First, get repository info to find default branch
                try:
                    repo_resp = await client.get(f"https://api.github.com/repos/{owner}/{repo}")
                    if repo_resp.is_success:
                        repo_info = repo_resp.json()
                        default_branch = repo_info.get("default_branch", "main")
                        print(f"[Security] Repository default branch: {default_branch}")
                except Exception as e:
                    print(f"[Security] Could not get repo info: {e}")
                
                # Get repository tree to find source files
                tree_data = None
                for branch in [default_branch, "main", "master"]:
                    try:
                        tree_resp = await client.get(
                            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
                        )
                        if tree_resp.is_success:
                            tree_data = tree_resp.json()
                            print(f"[Security] Successfully fetched tree from '{branch}' branch")
                            break
                    except Exception as e:
                        print(f"[Security] Failed to fetch tree from '{branch}': {e}")
                        continue
                
                if tree_data:
                    files = tree_data.get("tree", [])
                    print(f"[Security] Found {len(files)} total files in repository")
                    
                    # Filter for source code files with more extensions and larger size limit
                    source_extensions = [
                        '.py', '.js', '.java', '.go', '.ts', '.jsx', '.tsx', '.php', '.rb', 
                        '.c', '.cpp', '.cs', '.rs', '.kt', '.swift', '.m', '.h', '.scala',
                        '.sql', '.sh', '.bash', '.yaml', '.yml', '.json', '.xml'
                    ]
                    source_files = [
                        f for f in files 
                        if f.get("type") == "blob" and 
                        any(f.get("path", "").endswith(ext) for ext in source_extensions) and
                        f.get("size", 0) < 500000 and  # Increased to 500KB
                        f.get("size", 0) > 0 and  # Skip empty files
                        not any(skip in f.get("path", "") for skip in [
                            'node_modules/', 'vendor/', 'dist/', 'build/', '.min.', 
                            'package-lock.json', 'yarn.lock', '__pycache__/'
                        ])
                    ]
                    
                    print(f"[Security] Found {len(source_files)} source code files")
                    
                    # Prioritize certain files and limit total
                    priority_files = [f for f in source_files if any(p in f.get("path", "").lower() for p in ['main', 'app', 'index', 'server', 'api', 'auth', 'config'])]
                    other_files = [f for f in source_files if f not in priority_files]
                    
                    # Take up to 3 priority files + up to 7 other files = max 10 files
                    files_to_fetch = (priority_files[:3] + other_files[:7])[:10]
                    
                    print(f"[Security] Fetching content from {len(files_to_fetch)} files")
                    
                    # Fetch content of each source file
                    for file_info in files_to_fetch:
                        try:
                            file_path = file_info.get("path", "")
                            file_size = file_info.get("size", 0)
                            print(f"[Security] Fetching: {file_path} ({file_size} bytes)")
                            
                            file_resp = await client.get(
                                f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
                            )
                            if file_resp.is_success:
                                file_data = file_resp.json()
                                if "content" in file_data:
                                    file_content = base64.b64decode(file_data["content"]).decode('utf-8', errors='ignore')
                                    # Limit individual file content to 5000 chars
                                    if len(file_content) > 5000:
                                        file_content = file_content[:5000] + f"\n... (truncated {len(file_content) - 5000} chars)"
                                    code_parts.append(f"# File: {file_path}\n{file_content}")
                        except Exception as e:
                            print(f"[Security] Error fetching {file_path}: {e}")
                            continue
            
            print(f"[Security] Successfully fetched {len(code_parts)} files with total {sum(len(c) for c in code_parts)} characters")
            
            if not code_parts:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unable to fetch source code files from repository '{owner}/{repo}'. Repository may be empty, contain only non-code files, or all files exceed size limits. Try a different repository."
                )
            
            code_to_analyze = "\n\n".join(code_parts)
        
        # Handle direct code input
        else:
            if not request.code or not request.code.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Code cannot be empty"
                )
            code_to_analyze = request.code
        
        # Perform hybrid security analysis
        result = await analyze_code_security(
            code=code_to_analyze,
            language="auto"
        )
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Security API] Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Security analysis failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for security auditor service."""
    return {
        "status": "healthy",
        "service": "Security Auditor API",
        "features": [
            "Static pattern matching",
            "AI-powered analysis",
            "RAG-enhanced detection",
            "OWASP Top 10 coverage"
        ]
    }


@router.get("/vulnerability-types")
async def get_vulnerability_types():
    """
    Get list of vulnerability types that can be detected.
    
    Returns information about each vulnerability category including:
    - Type name
    - Severity level
    - OWASP category
    - CWE mapping
    """
    
    from app.core.security_agent import VULNERABILITY_PATTERNS
    
    vulnerability_info = []
    for vuln_type, config in VULNERABILITY_PATTERNS.items():
        vulnerability_info.append({
            "type": vuln_type,
            "severity": config["severity"],
            "category": config["category"],
            "pattern_count": len(config["patterns"]),
            "detection_method": "static + AI"
        })
    
    return {
        "total_types": len(vulnerability_info),
        "vulnerabilities": vulnerability_info,
        "owasp_coverage": [
            "A01:2021 - Broken Access Control",
            "A02:2021 - Cryptographic Failures",
            "A03:2021 - Injection",
            "A05:2021 - Security Misconfiguration",
            "A07:2021 - Authentication Failures",
            "A08:2021 - Software and Data Integrity Failures",
            "A09:2021 - Security Logging Failures",
            "A10:2021 - Server-Side Request Forgery"
        ]
    }


@router.post("/batch-analyze")
async def batch_analyze(files: list[SecurityAuditInput]):
    """
    Analyze multiple files in a single request.
    
    **Example Request:**
    ```json
    [
        {
            "code": "...",
            "language": "python",
            "file_name": "app.py"
        },
        {
            "code": "...",
            "language": "javascript",
            "file_name": "script.js"
        }
    ]
    ```
    
    **Returns:**
    List of security audit results for each file.
    """
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 files allowed per batch request"
        )
    
    results = []
    for file_input in files:
        try:
            result = await analyze_code_security(
                code=file_input.code,
                language=file_input.language or "python"
            )
            results.append({
                "file_name": file_input.file_name or "unknown",
                "analysis": result.dict()
            })
        except Exception as e:
            results.append({
                "file_name": file_input.file_name or "unknown",
                "error": str(e)
            })
    
    return {
        "total_files": len(files),
        "results": results
    }
