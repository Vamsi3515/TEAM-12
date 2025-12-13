import json
import os
import httpx
from fastapi import HTTPException
from typing import Any, Dict, List
from app.core.llm_client import call_chat, _call_gemini, _call_groq
from app.core.vectorstore import get_or_create_collection
from app.core.embeddings import embed
from app.core.github_rag_data import github_knowledge
from app.models.schemas import GitHubAnalyzeOutput, GitHubMetric

GITHUB_API = "https://api.github.com"


# ============================================================================
# FUNCTION 1: Seed Knowledge Base into ChromaDB (One-time Setup)
# ============================================================================

def seed_knowledge_base():
    """
    Seed the ChromaDB vector store with GitHub best practices knowledge.
    This is a one-time setup function that populates the knowledge base.
    
    Returns:
        int: Number of documents seeded
    """
    try:
        # Get or create the ChromaDB collection
        collection = get_or_create_collection()
        
        # Check if already seeded
        existing_count = collection.count()
        if existing_count > 0:
            print(f"Knowledge base already seeded with {existing_count} documents")
            return existing_count
        
        # Prepare documents for embedding
        documents = []
        metadatas = []
        ids = []
        
        for idx, item in enumerate(github_knowledge):
            documents.append(item["content"])
            metadatas.append({
                "category": item.get("category", "general"),
                "topic": item.get("topic", "unknown")
            })
            ids.append(f"doc_{idx}")
        
        # Embed and add to collection
        embeddings = [embed(doc) for doc in documents]
        
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Successfully seeded {len(documents)} documents into knowledge base")
        return len(documents)
        
    except Exception as e:
        print(f"Error seeding knowledge base: {e}")
        raise


# ============================================================================
# FUNCTION 2: Fetch Comprehensive Repo Data from GitHub API
# ============================================================================

async def fetch_github_repo_data(repo_url: str) -> Dict[str, Any]:
    """
    Fetch comprehensive repository data from GitHub API including:
    - Basic metadata (stars, forks, language)
    - README content
    - Recent commit activity
    - Languages breakdown
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        
    Returns:
        Dict containing all fetched repository data
        
    Raises:
        HTTPException: If GitHub API call fails
    """
    try:
        # Extract owner and repo from URL
        parts = repo_url.rstrip('/').replace('.git', '').split('/')
        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL format")
        
        owner, repo = parts[-2], parts[-1]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch basic repo info
            repo_response = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}")
            if repo_response.status_code != 200:
                raise HTTPException(
                    status_code=repo_response.status_code,
                    detail=f"GitHub API error: {repo_response.text}"
                )
            
            repo_data = repo_response.json()
            
            # Fetch README
            readme_content = ""
            try:
                readme_response = await client.get(
                    f"{GITHUB_API}/repos/{owner}/{repo}/readme",
                    headers={"Accept": "application/vnd.github.raw"}
                )
                if readme_response.status_code == 200:
                    readme_content = readme_response.text[:5000]  # Limit to 5000 chars
            except Exception as e:
                print(f"Could not fetch README: {e}")
            
            # Fetch recent commits (last 10)
            commits_data = []
            try:
                commits_response = await client.get(
                    f"{GITHUB_API}/repos/{owner}/{repo}/commits",
                    params={"per_page": 10}
                )
                if commits_response.status_code == 200:
                    commits = commits_response.json()
                    commits_data = [
                        {
                            "message": c["commit"]["message"][:100],
                            "date": c["commit"]["author"]["date"]
                        }
                        for c in commits[:10]
                    ]
            except Exception as e:
                print(f"Could not fetch commits: {e}")
            
            # Fetch languages
            languages_data = {}
            try:
                lang_response = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}/languages")
                if lang_response.status_code == 200:
                    languages_data = lang_response.json()
            except Exception as e:
                print(f"Could not fetch languages: {e}")
            
            # Compile all data
            result = {
                "name": repo_data.get("name", ""),
                "full_name": repo_data.get("full_name", ""),
                "description": repo_data.get("description", "No description available"),
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "watchers": repo_data.get("watchers_count", 0),
                "open_issues": repo_data.get("open_issues_count", 0),
                "language": repo_data.get("language", "Unknown"),
                "languages": languages_data,
                "size": repo_data.get("size", 0),
                "created_at": repo_data.get("created_at", ""),
                "updated_at": repo_data.get("updated_at", ""),
                "pushed_at": repo_data.get("pushed_at", ""),
                "license": repo_data.get("license", {}).get("name", "No license") if repo_data.get("license") else "No license",
                "topics": repo_data.get("topics", []),
                "has_wiki": repo_data.get("has_wiki", False),
                "has_issues": repo_data.get("has_issues", False),
                "has_projects": repo_data.get("has_projects", False),
                "readme": readme_content,
                "recent_commits": commits_data,
                "default_branch": repo_data.get("default_branch", "main"),
            }
            
            return result
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching GitHub data: {str(e)}")


# ============================================================================
# FUNCTION 3: RAG Retrieval - Search Vector Store for Best Practices
# ============================================================================

def retrieve_relevant_practices(query: str, n_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve relevant best practices from the vector store using RAG.
    
    Args:
        query: Search query (e.g., "Python FastAPI best practices")
        n_results: Number of results to retrieve (default: 5)
        
    Returns:
        Dict containing:
            - documents: List of retrieved text snippets
            - ids: List of document IDs
            - metadatas: List of metadata dicts
            - formatted_context: Formatted string for LLM prompt
    """
    try:
        # Get the collection
        collection = get_or_create_collection()
        
        # Check if collection is empty
        if collection.count() == 0:
            print("Warning: Knowledge base is empty. Seeding now...")
            seed_knowledge_base()
        
        # Embed the query
        query_embedding = embed(query)
        
        # Query the vector store
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Extract results
        documents = results['documents'][0] if results['documents'] else []
        ids = results['ids'][0] if results['ids'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        
        # Format context for LLM prompt
        formatted_context = "\n\n".join([
            f"[Source {i+1} - {ids[i]}]:\n{doc}"
            for i, doc in enumerate(documents)
        ])
        
        return {
            "documents": documents,
            "ids": ids,
            "metadatas": metadatas,
            "formatted_context": formatted_context
        }
        
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return {
            "documents": [],
            "ids": [],
            "metadatas": [],
            "formatted_context": "No relevant best practices found."
        }


# ============================================================================
# FUNCTION 4: Main Analyzer - Orchestrates Everything Together
# ============================================================================

async def analyze_github_repository(repo_url: str) -> GitHubAnalyzeOutput:
    """
    Main orchestrator function that:
    1. Fetches GitHub repo data
    2. Retrieves relevant best practices via RAG
    3. Builds an analysis prompt
    4. Calls LLM for analysis
    5. Returns structured output with evidence
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        GitHubAnalyzeOutput: Complete analysis with metrics, strengths, weaknesses, suggestions, and RAG evidence
    """
    try:
        # STEP 1: Fetch comprehensive repo data from GitHub API
        print(f"Fetching data for: {repo_url}")
        repo_data = await fetch_github_repo_data(repo_url)
        
        # STEP 2: Build RAG query based on repo characteristics
        primary_language = repo_data.get('language', 'general')
        topics = repo_data.get('topics', [])
        
        rag_query = f"Best practices for {primary_language} projects"
        if topics:
            rag_query += f" with focus on {', '.join(topics[:3])}"
        rag_query += ". Code quality, documentation, maintainability, testing."
        
        # STEP 3: Retrieve relevant best practices using RAG
        print(f"Retrieving best practices with query: {rag_query}")
        rag_results = retrieve_relevant_practices(rag_query, n_results=5)
        
        # STEP 4: Build comprehensive analysis prompt
        prompt = f"""You are an expert code reviewer analyzing a GitHub repository.

REPOSITORY INFORMATION:
- Name: {repo_data['full_name']}
- Description: {repo_data['description']}
- Primary Language: {repo_data['language']}
- Stars: {repo_data['stars']} | Forks: {repo_data['forks']} | Open Issues: {repo_data['open_issues']}
- License: {repo_data['license']}
- Topics: {', '.join(repo_data['topics']) if repo_data['topics'] else 'None'}
- Languages Used: {', '.join(repo_data['languages'].keys()) if repo_data['languages'] else 'N/A'}
- Last Updated: {repo_data['updated_at']}

README EXCERPT:
{repo_data['readme'][:1000] if repo_data['readme'] else 'No README available'}

RECENT COMMIT ACTIVITY:
{chr(10).join([f"- {c['message']} ({c['date']})" for c in repo_data['recent_commits'][:5]])}

RELEVANT BEST PRACTICES (from knowledge base):
{rag_results['formatted_context']}

Based on the repository information and best practices above, provide a comprehensive analysis in JSON format:

{{
  "tech_stack": ["List primary technologies, frameworks, and tools"],
  "metrics": [
    {{"name": "Code Quality", "score": 0-100, "explanation": "Detailed assessment"}},
    {{"name": "Documentation", "score": 0-100, "explanation": "Detailed assessment"}},
    {{"name": "Maintainability", "score": 0-100, "explanation": "Detailed assessment"}},
    {{"name": "Community & Activity", "score": 0-100, "explanation": "Detailed assessment"}},
    {{"name": "Best Practices Adherence", "score": 0-100, "explanation": "Detailed assessment"}}
  ],
  "strengths": ["List 3-5 key strengths with specific examples"],
  "weaknesses": ["List 3-5 areas needing improvement with specific examples"],
  "suggestions": ["List 3-5 actionable improvement recommendations"],
  "repo_summary": "A comprehensive 2-3 sentence summary of the repository's purpose and quality"
}}

Return ONLY valid JSON, no additional text or markdown."""
        
        # STEP 5: Call LLM for analysis
        print("Calling LLM for analysis...")
        llm_response = await call_chat(prompt)
        
        # STEP 6: Parse JSON response
        try:
            # Clean response if wrapped in markdown
            response_text = llm_response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            analysis_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            # Fallback response
            analysis_data = {
                "tech_stack": [repo_data['language']],
                "metrics": [
                    {"name": "Analysis Error", "score": 0, "explanation": "Failed to parse LLM response"}
                ],
                "strengths": ["Repository exists"],
                "weaknesses": ["Could not complete full analysis"],
                "suggestions": ["Retry analysis"],
                "repo_summary": repo_data['description']
            }
        
        # STEP 7: Build structured output with RAG evidence
        metrics = [
            GitHubMetric(
                name=m["name"],
                score=float(m["score"]),
                explanation=m["explanation"]
            )
            for m in analysis_data.get("metrics", [])
        ]
        
        # Build evidence snippets in required format
        evidence_snippets = [
            {"id": doc_id, "snippet": doc[:300]}  # First 300 chars
            for doc_id, doc in zip(rag_results['ids'], rag_results['documents'])
        ]
        
        output = GitHubAnalyzeOutput(
            tech_stack=analysis_data.get("tech_stack", [repo_data['language']]),
            metrics=metrics,
            strengths=analysis_data.get("strengths", []),
            weaknesses=analysis_data.get("weaknesses", []),
            suggestions=analysis_data.get("suggestions", []),
            repo_summary=analysis_data.get("repo_summary", repo_data['description']),
            evidence_ids=rag_results['ids'],
            evidence_snippets=evidence_snippets
        )
        
        print("Analysis completed successfully!")
        return output
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

