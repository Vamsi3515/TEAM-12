import json
import os
import httpx
from fastapi import HTTPException
from typing import Any, Dict, List
from app.core.Utils.llm_client import call_chat, _call_gemini, _call_groq
from app.core.RAGANDEMBEDDINGS.vectorstore import get_or_create_collection
from app.core.RAGANDEMBEDDINGS.embeddings import embed
from app.core.RAGANDEMBEDDINGS.github_rag_data import github_knowledge

GITHUB_API = "https://api.github.com"


def parse_owner_repo(repo_url: str):
    """Normalize GitHub URL/slug into (owner, repo) or raise ValueError."""
    if not repo_url or not repo_url.strip():
        raise ValueError("Provide a GitHub repository URL or slug like owner/repo")

    cleaned = repo_url.strip()
    cleaned = cleaned.replace("git@github.com:", "github.com/")
    cleaned = cleaned.replace("git://github.com/", "github.com/")
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        cleaned = cleaned.split("://", 1)[1]
    cleaned = cleaned.lstrip("www.")
    if cleaned.startswith("github.com/"):
        cleaned = cleaned[len("github.com/"):]
    cleaned = cleaned.rstrip("/").replace(".git", "")

    parts = [p for p in cleaned.split("/") if p]
    if len(parts) < 2:
        raise ValueError("Provide a GitHub repository in the form owner/repo")

    return parts[0], parts[1]


# -------------------- Seed RAG --------------------
def seed_github_collection(name="github_knowledge"):
    col = get_or_create_collection(name)
    if col.count() == 0:
        texts = [x["text"] for x in github_knowledge]
        ids = [x["id"] for x in github_knowledge]
        emb = embed(texts)
        col.add(documents=texts, ids=ids, embeddings=emb)
    return col


# -------------------- GitHub API fetch --------------------
async def fetch_github_repo(repo_url: str):
    """
    Accepts typical GitHub inputs:
    - https://github.com/owner/repo
    - github.com/owner/repo
    - owner/repo
    """
    try:
        owner, repo = parse_owner_repo(repo_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT")
    base_headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "fastapi/1.0",
    }
    if github_token:
        base_headers["Authorization"] = f"Bearer {github_token}"

    async with httpx.AsyncClient(timeout=30, headers=base_headers) as client:
        try:
            repo_resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}")
            repo_resp.raise_for_status()
            repo_data = repo_resp.json()
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code if exc.response else 500
            if status == 403:
                detail = "GitHub API returned 403 (rate limit or private repo). Set GITHUB_TOKEN/GITHUB_PAT for authenticated requests."
            else:
                detail = f"GitHub API returned {status} for {owner}/{repo}"
            raise HTTPException(status_code=status, detail=detail)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"GitHub API request failed: {exc}")

        readme_data = {}
        try:
            readme_resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}/readme")
            if readme_resp.is_success:
                readme_data = readme_resp.json()
        except Exception:
            readme_data = {}

        languages = {}
        try:
            langs_resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}/languages")
            if langs_resp.is_success:
                languages = langs_resp.json()
        except Exception:
            languages = {}

        commits = []
        try:
            commits_resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}/commits")
            if commits_resp.is_success:
                commits_json = commits_resp.json()
                if isinstance(commits_json, list):
                    commits = commits_json
        except Exception:
            commits = []

    # extract README text if base64 encoded
    readme_text = ""
    if "content" in readme_data:
        import base64
        readme_text = base64.b64decode(readme_data["content"]).decode("utf-8", errors="ignore")

    return {
        "repo": repo_data,
        "readme": readme_text,
        "languages": languages,
        "commits": commits[:20]  # limit
    }


# -------------------- GitHub Profile fetch (for Authenticity Agent) --------------------
async def fetch_github_profile(username: str) -> Dict[str, Any]:
    """
    Fetch aggregated GitHub profile data for authenticity analysis.
    Returns data matching GitHubEvidence model format:
    - languages: aggregated across all repos
    - repo_count: total public repos
    - commit_frequency: commits in last year
    - readme_quality: average quality assessment
    - contribution_pattern: based on commit distribution
    - top_projects: sorted by stars
    """
    if not username or not username.strip():
        raise HTTPException(status_code=400, detail="Provide a GitHub username")
    
    username = username.strip().lstrip("@")
    github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT")
    base_headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "fastapi/1.0",
    }
    if github_token:
        base_headers["Authorization"] = f"Bearer {github_token}"
    
    async with httpx.AsyncClient(timeout=30, headers=base_headers) as client:
        # 1. Get user profile
        try:
            user_resp = await client.get(f"{GITHUB_API}/users/{username}")
            user_resp.raise_for_status()
            user_data = user_resp.json()
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code if exc.response else 500
            if status == 403:
                detail = "GitHub API returned 403 (rate limit). Set GITHUB_TOKEN/GITHUB_PAT for authenticated requests."
            elif status == 404:
                detail = f"GitHub user '{username}' not found"
            else:
                detail = f"GitHub API returned {status} for user {username}"
            raise HTTPException(status_code=status, detail=detail)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"GitHub API request failed: {exc}")
        
        repo_count = user_data.get("public_repos", 0)
        
        # 2. Get user's repos (limited to first 100 for performance)
        repos = []
        try:
            repos_resp = await client.get(
                f"{GITHUB_API}/users/{username}/repos",
                params={"sort": "updated", "per_page": 100}
            )
            if repos_resp.is_success:
                repos = repos_resp.json()
        except Exception:
            repos = []
        
        # 3. Aggregate languages across all repos
        language_counts = {}
        for repo in repos:
            if repo.get("fork"):  # Skip forks
                continue
            try:
                lang_resp = await client.get(f"{GITHUB_API}/repos/{username}/{repo['name']}/languages")
                if lang_resp.is_success:
                    langs = lang_resp.json()
                    for lang, bytes_count in langs.items():
                        language_counts[lang] = language_counts.get(lang, 0) + bytes_count
            except Exception:
                continue
        
        # Sort languages by usage
        sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
        languages = [lang for lang, _ in sorted_langs[:10]]  # Top 10 languages
        
        # 4. Estimate commit frequency (from user events API)
        commit_count_last_year = 0
        try:
            events_resp = await client.get(
                f"{GITHUB_API}/users/{username}/events/public",
                params={"per_page": 100}
            )
            if events_resp.is_success:
                events = events_resp.json()
                # Count PushEvents in last year
                from datetime import datetime, timedelta
                one_year_ago = datetime.now() - timedelta(days=365)
                for event in events:
                    if event.get("type") == "PushEvent":
                        created_at = event.get("created_at", "")
                        try:
                            event_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                            if event_date > one_year_ago:
                                # Each PushEvent can contain multiple commits
                                commits = event.get("payload", {}).get("commits", [])
                                commit_count_last_year += len(commits) if commits else 1
                        except:
                            continue
        except Exception:
            pass
        
        # Categorize commit frequency
        if commit_count_last_year >= 500:
            commit_frequency = f"Very Active - {commit_count_last_year}+ commits in last year"
        elif commit_count_last_year >= 200:
            commit_frequency = f"Active - {commit_count_last_year} commits in last year"
        elif commit_count_last_year >= 100:
            commit_frequency = f"Moderate - {commit_count_last_year} commits in last year"
        elif commit_count_last_year > 0:
            commit_frequency = f"Low - {commit_count_last_year} commits in last year"
        else:
            commit_frequency = "None"
        
        # 5. Assess README quality (sample top repos)
        readme_scores = []
        for repo in repos[:10]:  # Check top 10 repos
            if repo.get("fork"):
                continue
            try:
                readme_resp = await client.get(
                    f"{GITHUB_API}/repos/{username}/{repo['name']}/readme"
                )
                if readme_resp.is_success:
                    readme_data = readme_resp.json()
                    content = readme_data.get("content", "")
                    import base64
                    readme_text = base64.b64decode(content).decode("utf-8", errors="ignore")
                    
                    # Simple quality heuristic
                    length = len(readme_text)
                    if length > 2000:
                        readme_scores.append(4)  # Excellent
                    elif length > 1000:
                        readme_scores.append(3)  # Good
                    elif length > 300:
                        readme_scores.append(2)  # Fair
                    else:
                        readme_scores.append(1)  # Poor
            except Exception:
                continue
        
        # Average README quality
        if readme_scores:
            avg_score = sum(readme_scores) / len(readme_scores)
            if avg_score >= 3.5:
                readme_quality = "Excellent - detailed documentation"
            elif avg_score >= 2.5:
                readme_quality = "Good - basic documentation"
            elif avg_score >= 1.5:
                readme_quality = "Fair - minimal documentation"
            else:
                readme_quality = "Poor - minimal documentation"
        else:
            readme_quality = "N/A"
        
        # 6. Contribution pattern (based on commit distribution)
        if commit_count_last_year >= 250:
            contribution_pattern = "Consistent - daily commits"
        elif commit_count_last_year >= 100:
            contribution_pattern = "Periodic - weekly commits"
        elif commit_count_last_year >= 50:
            contribution_pattern = "Growing - increasing activity"
        elif commit_count_last_year > 0:
            contribution_pattern = "Sporadic - monthly commits"
        else:
            contribution_pattern = "No public activity"
        
        # 7. Top projects (sorted by stars)
        top_projects = []
        sorted_repos = sorted(
            [r for r in repos if not r.get("fork")],
            key=lambda x: x.get("stargazers_count", 0),
            reverse=True
        )
        for repo in sorted_repos[:5]:  # Top 5 projects
            top_projects.append({
                "name": repo.get("name", ""),
                "language": repo.get("language", "Unknown"),
                "stars": repo.get("stargazers_count", 0),
                "description": repo.get("description", "") or "No description"
            })
    
    return {
        "username": username,
        "languages": languages,
        "repo_count": repo_count,
        "commit_frequency": commit_frequency,
        "readme_quality": readme_quality,
        "contribution_pattern": contribution_pattern,
        "top_projects": top_projects,
        "raw_profile_data": {
            "name": user_data.get("name"),
            "bio": user_data.get("bio"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "created_at": user_data.get("created_at"),
        }
    }


# -------------------- RAG retrieval --------------------
def get_rag_context(query: str, collection_name="github_knowledge"):
    col = seed_github_collection(collection_name)
    q_emb = embed([query])[0]
    res = col.query(query_embeddings=[q_emb], n_results=3)

    docs = res.get("documents", [[]])[0] if res else []
    ids = res.get("ids", [[]])[0] if res else []

    rag = []
    for i, d in enumerate(docs):
        rag.append({"id": ids[i], "text": d})

    rag_context = "\n\n".join([f"ID:{x['id']}\n{x['text']}" for x in rag])
    return rag, rag_context


# -------------------- LLM Analyzer --------------------
async def analyze_github_repo(repo_url: str):

    # 1. Fetch repo data
    repo_data = await fetch_github_repo(repo_url)
    readme = repo_data["readme"]
    languages = repo_data["languages"]
    commits = repo_data["commits"]

    # 2. Prepare RAG
    rag_docs, rag_context = get_rag_context(repo_url)

    # Build tech stack summary
    tech_stack_list = list(languages.keys()) if languages else []
    commit_messages = [c.get('commit', {}).get('message', 'No message') for c in commits[:10]]

    # 3. Build LLM Prompt
    prompt = f"""You are a professional code reviewer analyzing a GitHub repository.

Repository URL: {repo_url}

Tech Stack (from GitHub API):
{json.dumps(tech_stack_list, indent=2)}

README excerpt:
{readme[:3000] if readme else "No README available"}

Recent commit messages:
{json.dumps(commit_messages, indent=2)}

Best Practices (RAG Knowledge):
{rag_context}

Analyze this repository and return ONLY valid JSON matching this EXACT structure:
{{
  "tech_stack": ["Python", "JavaScript", "etc"],
  "metrics": [
    {{
      "name": "Code Quality",
      "score": 75,
      "explanation": "why this score"
    }},
    {{
      "name": "Documentation",
      "score": 60,
      "explanation": "why this score"
    }}
  ],
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "suggestions": ["suggestion 1", "suggestion 2"],
  "repo_summary": "A brief summary of the repository purpose and quality"
}}

CRITICAL: Return ONLY the JSON object. No markdown, no code fences, no extra text.
"""

    raw = await _call_groq(prompt, model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=3500)

    # Clean markdown fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    # JSON parse with retry
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to fix with LLM
        fix_prompt = f"""Convert this to valid JSON matching the schema:
{{
  "tech_stack": [],
  "metrics": [{{"name": "", "score": 0, "explanation": ""}}],
  "strengths": [],
  "weaknesses": [],
  "suggestions": [],
  "repo_summary": ""
}}

Input to fix:
{cleaned}

Return ONLY valid JSON, no markdown fences."""
        try:
            fix = await call_chat(fix_prompt, temperature=0.1, max_tokens=1500)
            fix = fix.strip()
            if fix.startswith("```"):
                lines = fix.split("\n")
                lines = [l for l in lines if not l.strip().startswith("```")]
                fix = "\n".join(lines).strip()
            parsed = json.loads(fix)
        except:
            # Fallback to minimal valid structure
            parsed = {
                "tech_stack": tech_stack_list,
                "metrics": [
                    {"name": "Code Quality", "score": 50, "explanation": "Unable to analyze"},
                    {"name": "Documentation", "score": 50, "explanation": "Unable to analyze"}
                ],
                "strengths": ["Repository exists"],
                "weaknesses": ["Analysis incomplete"],
                "suggestions": ["Add more documentation", "Improve code structure"],
                "repo_summary": f"Repository at {repo_url} with {len(tech_stack_list)} languages"
            }

    # Ensure all required fields with defaults
    parsed.setdefault("tech_stack", tech_stack_list)
    parsed.setdefault("metrics", [{"name": "Overall", "score": 50, "explanation": "Default"}])
    parsed.setdefault("strengths", ["Repository exists"])
    parsed.setdefault("weaknesses", ["Analysis incomplete"])
    parsed.setdefault("suggestions", ["Review code structure"])
    parsed.setdefault("repo_summary", f"Repository analysis for {repo_url}")

    # Add evidence from RAG
    parsed["evidence_ids"] = [x["id"] for x in rag_docs]
    parsed["evidence_snippets"] = [
        {"id": x["id"], "snippet": x["text"][:300]} for x in rag_docs
    ]

    # Enrich tech_stack from primary language if empty
    if not parsed.get("tech_stack"):
        primary_lang = (repo_data.get("repo") or {}).get("language")
        if primary_lang:
            parsed["tech_stack"] = [primary_lang]
        else:
            parsed["tech_stack"] = ["Unknown"]

    # Add heuristic Complexity metric if missing
    metrics = parsed.get("metrics") or []
    has_complexity = any((m.get("name", "").lower() == "complexity") for m in metrics)
    if not has_complexity:
        size_kb = (repo_data.get("repo") or {}).get("size") or 0
        complexity_score = max(10, min(100, int(size_kb / 50)))
        metrics.append({
            "name": "Complexity",
            "score": complexity_score,
            "explanation": "Heuristic from GitHub reported repo size (KB)."
        })
        parsed["metrics"] = metrics

    return parsed