import json
from app.core.llm_client import call_chat
from app.core.vectorstore import get_or_create_collection
from app.core.embeddings import embed
from app.core.learning_rag_data import learning_knowledge

def seed_learning_collection():
    """Seed learning knowledge into vector database for RAG."""
    col = get_or_create_collection("learning_knowledge")
    if col.count() == 0:
        texts = [x["text"] for x in learning_knowledge]
        ids = [x["id"] for x in learning_knowledge]
        emb = embed(texts)
        col.add(documents=texts, ids=ids, embeddings=emb)
    return col

def get_learning_rag_context(query: str):
    """Retrieve relevant learning guidance from RAG."""
    col = seed_learning_collection()
    q_emb = embed([query])[0]
    res = col.query(query_embeddings=[q_emb], n_results=3)

    docs = res["documents"][0]
    ids = res["ids"][0]

    context = "\n\n".join([f"ID:{ids[i]}\n{docs[i]}" for i in range(len(docs))])
    rag_docs = [{"id": ids[i], "text": docs[i]} for i in range(len(docs))]

    return context, rag_docs

async def generate_learning_flow(topic: str, experience_level: str = "beginner", weekly_hours: str = "5-10"):
    """Generate learning flow matching frontend expectations with RAG enhancement."""
    
    # Calculate timeline based on weekly hours
    hours_map = {"1-5": 3, "5-10": 7, "10-20": 15, "20+": 25}
    avg_hours = hours_map.get(weekly_hours, 7)
    
    # Estimate total weeks (adjust based on experience level)
    level_multiplier = {"beginner": 1.5, "intermediate": 1.0, "advanced": 0.7}
    multiplier = level_multiplier.get(experience_level, 1.0)
    estimated_weeks = int(12 * multiplier)
    
    # Get RAG context for curriculum design best practices
    query = f"{topic} {experience_level} learning path curriculum"
    rag_context, rag_docs = get_learning_rag_context(query)
    
    prompt = f"""You are an expert curriculum designer. Create a COMPLETE, DETAILED learning roadmap for: "{topic}"

Experience Level: {experience_level}
Weekly Study Hours: {weekly_hours}
Estimated Timeline: {estimated_weeks} weeks

Curriculum Design Best Practices (from knowledge base):
{rag_context}

Generate a comprehensive learning plan in STRICT JSON format with NO markdown fences.

IMPORTANT: Fill ALL arrays with real, detailed content. Do not return empty arrays.

Required JSON structure:
{{
  "phases": [
    {{
      "name": "Phase 1: Foundations",
      "duration": "4 weeks",
      "description": "Master the fundamentals and set up your development environment",
      "keyTopics": ["Installation & Setup", "Basic Syntax", "Data Types", "Control Flow", "Functions"]
    }},
    {{
      "name": "Phase 2: Intermediate Concepts",
      "duration": "5 weeks",
      "description": "Build practical skills with real-world applications",
      "keyTopics": ["OOP Principles", "Data Structures", "File I/O", "Error Handling", "APIs"]
    }},
    {{
      "name": "Phase 3: Advanced Techniques",
      "duration": "4 weeks",
      "description": "Learn advanced patterns and best practices",
      "keyTopics": ["Design Patterns", "Testing", "Performance", "Security", "Deployment"]
    }},
    {{
      "name": "Phase 4: Real-World Projects",
      "duration": "5 weeks",
      "description": "Build portfolio-worthy applications",
      "keyTopics": ["Full-Stack Project", "Database Integration", "Authentication", "CI/CD", "Production"]
    }}
  ],
  "mermaidDiagram": "graph TD\n  A[Start Learning] --> B[Phase 1: Foundations]\n  B --> C[Phase 2: Intermediate]\n  C --> D[Phase 3: Advanced]\n  D --> E[Phase 4: Projects]\n  E --> F[Job Ready]",
  "youtubeChannels": [
    {{
      "name": "freeCodeCamp",
      "url": "https://youtube.com/@freecodecamp",
      "focus": "Comprehensive full-length courses and tutorials",
      "recommendedPlaylists": ["{topic} Full Course", "Beginner to Advanced", "Project-Based Learning"]
    }},
    {{
      "name": "Traversy Media",
      "url": "https://youtube.com/@TraversyMedia",
      "focus": "Practical crash courses and project builds",
      "recommendedPlaylists": ["{topic} Crash Course", "Build Real Projects", "Modern Development"]
    }},
    {{
      "name": "The Net Ninja",
      "url": "https://youtube.com/@NetNinja",
      "focus": "Step-by-step tutorial series",
      "recommendedPlaylists": ["{topic} Tutorial Series", "From Scratch", "Best Practices"]
    }}
  ],
  "projects": [
    {{
      "name": "Simple {topic} Calculator",
      "description": "Build a basic calculator to understand core concepts and syntax",
      "difficulty": "beginner",
      "estimatedHours": 8
    }},
    {{
      "name": "Task Manager Application",
      "description": "Create a CRUD app with database integration",
      "difficulty": "intermediate",
      "estimatedHours": 20
    }},
    {{
      "name": "Weather Dashboard",
      "description": "Build an app consuming external APIs with real-time data",
      "difficulty": "intermediate",
      "estimatedHours": 25
    }},
    {{
      "name": "Full-Stack E-commerce Platform",
      "description": "Complete marketplace with authentication, payments, and admin panel",
      "difficulty": "advanced",
      "estimatedHours": 60
    }}
  ],
  "timeline": "Complete in {estimated_weeks} weeks with {weekly_hours} hours per week for a total of approximately {int(estimated_weeks * 7.5)} hours",
  "prerequisites": ["Basic computer literacy", "Text editor installed", "Internet connection", "Dedication and consistency"],
  "resources": {{
    "books": ["Official {topic} Documentation", "Eloquent JavaScript (if web)", "Clean Code by Robert Martin", "{topic} Cookbook"],
    "websites": ["Official Documentation", "MDN Web Docs", "Stack Overflow", "Dev.to", "Medium tutorials"],
    "communities": ["r/{topic.lower().replace(' ', '')} on Reddit", "{topic} Discord Server", "Stack Overflow", "Dev.to Community", "GitHub Discussions"]
  }}
}}

CRITICAL RULES:
1. Return ONLY raw JSON, NO markdown fences, NO extra text
2. Include EXACTLY 4-5 learning phases with detailed keyTopics (5+ topics each)
3. Create a valid Mermaid flowchart using graph TD syntax with proper newlines (\n not \\n)
4. Include 3-5 REAL YouTube channels with actual working URLs
5. Include 4-6 projects from beginner to advanced with specific names
6. Fill ALL resource arrays with real, relevant items (3-5 items minimum each)
7. Prerequisites should list real requirements
8. Timeline should calculate total hours
9. Make descriptions specific to {topic}, not generic
10. Use the RAG knowledge above to structure your phases properly

Generate the COMPLETE JSON now:"""

    # Use Gemini for complex JSON generation (better than HF/Groq for structured output)
    from app.core.llm_client import _call_gemini
    raw_response = await _call_gemini(prompt, model="gemini-2.5-flash", max_tokens=4096, temperature=0.6)
    
    # Clean markdown fences
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()
    
    # Parse JSON
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"[Learning Agent] JSON parse error: {e}")
        print(f"[Learning Agent] Raw response: {cleaned[:500]}...")
        
        # Fallback structure
        parsed = {
            "phases": [
                {
                    "name": "Phase 1: Fundamentals",
                    "duration": f"{estimated_weeks // 3} weeks",
                    "description": f"Learn the core concepts of {topic}",
                    "keyTopics": ["Basics", "Core Concepts", "Syntax", "Variables", "Basic Operations"]
                },
                {
                    "name": "Phase 2: Intermediate Skills",
                    "duration": f"{estimated_weeks // 3} weeks",
                    "description": f"Build practical projects with {topic}",
                    "keyTopics": ["Advanced Features", "Best Practices", "Real Projects", "Testing", "Debugging"]
                },
                {
                    "name": "Phase 3: Mastery",
                    "duration": f"{estimated_weeks - 2 * (estimated_weeks // 3)} weeks",
                    "description": f"Become proficient in {topic}",
                    "keyTopics": ["Advanced Patterns", "Optimization", "Production Ready", "Security", "Deployment"]
                }
            ],
            "mermaidDiagram": f"graph TD\n  A[Start Learning {topic}] --> B[Phase 1: Fundamentals]\n  B --> C[Phase 2: Intermediate]\n  C --> D[Phase 3: Mastery]\n  D --> E[Complete]",
            "youtubeChannels": [
                {
                    "name": "freeCodeCamp",
                    "url": "https://youtube.com/@freecodecamp",
                    "focus": "Comprehensive tutorials and full courses",
                    "recommendedPlaylists": [f"{topic} Full Course", "Beginner Tutorial"]
                },
                {
                    "name": "Traversy Media",
                    "url": "https://youtube.com/@TraversyMedia",
                    "focus": "Practical web development tutorials",
                    "recommendedPlaylists": [f"{topic} Crash Course", "Project Builds"]
                },
                {
                    "name": "Net Ninja",
                    "url": "https://youtube.com/@NetNinja",
                    "focus": "Step-by-step coding tutorials",
                    "recommendedPlaylists": [f"{topic} Tutorial Series"]
                }
            ],
            "projects": [
                {
                    "name": f"Simple {topic} Application",
                    "description": "Build a basic application to understand fundamentals",
                    "difficulty": "beginner",
                    "estimatedHours": 10
                },
                {
                    "name": f"Intermediate {topic} Project",
                    "description": "Create a real-world application with multiple features",
                    "difficulty": "intermediate",
                    "estimatedHours": 25
                },
                {
                    "name": f"Advanced {topic} System",
                    "description": "Build a production-ready application",
                    "difficulty": "advanced",
                    "estimatedHours": 50
                }
            ],
            "timeline": f"Complete in {estimated_weeks} weeks with {weekly_hours} hours per week",
            "prerequisites": ["Basic computer skills", "Internet access", "Dedication to learn"],
            "resources": {
                "books": [f"Official {topic} Documentation", f"{topic} Best Practices Guide"],
                "websites": ["Official Documentation", "MDN Web Docs", "Stack Overflow"],
                "communities": ["Reddit community", "Discord servers", "GitHub Discussions"]
            }
        }
    
    # Validate required fields
    if "phases" not in parsed:
        parsed["phases"] = []
    if "mermaidDiagram" not in parsed:
        parsed["mermaidDiagram"] = f"graph TD\n  A[Start] --> B[Learn {topic}]\n  B --> C[Complete]"
    else:
        # Fix escaped newlines in mermaid diagrams
        parsed["mermaidDiagram"] = parsed["mermaidDiagram"].replace("\\n", "\n")
    if "youtubeChannels" not in parsed:
        parsed["youtubeChannels"] = []
    if "projects" not in parsed:
        parsed["projects"] = []
    if "timeline" not in parsed:
        parsed["timeline"] = f"{estimated_weeks} weeks with {weekly_hours} hours/week"
    if "prerequisites" not in parsed:
        parsed["prerequisites"] = []
    if "resources" not in parsed:
        parsed["resources"] = {"books": [], "websites": [], "communities": []}
    
    # Add RAG evidence for hackathon (shows RAG retrieval)
    parsed["evidence_ids"] = [d["id"] for d in rag_docs]
    parsed["evidence_snippets"] = [
        {"id": d["id"], "snippet": d["text"][:300]} for d in rag_docs
    ]
    
    return parsed
