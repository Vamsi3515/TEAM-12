# Code to UML Diagram Generator

## Overview
AI-powered system that converts source code into interactive UML diagrams using RAG (Retrieval-Augmented Generation) and LLM analysis.

## Features

### 🎯 Two Input Types
1. **Code Snippet**: Direct code input with language selection
2. **Repository URL**: GitHub repository analysis (coming soon)

### 🤖 Auto-Detection Logic
The system automatically detects appropriate diagram types based on code patterns:

- **Class Diagram**: Detected when code contains `class`, `interface`, `struct`, `def __init__`
- **Sequence Diagram**: Detected for method calls and object interactions
- **Flowchart**: Detected for control flow (`if`, `for`, `while`, `switch`)
- **ERD**: Detected for database models (`table`, `foreignkey`, `model`)
- **State Diagram**: Detected for state management patterns

### 📊 Supported Diagram Types
- Class Diagram
- Sequence Diagram
- Flowchart
- Entity Relationship Diagram (ERD)
- State Diagram

### 🌐 Supported Languages
- Python
- JavaScript
- TypeScript
- Java
- C#
- C++
- Go

## Architecture

### Backend Processing Workflow

```
┌─────────────────┐
│  User Input     │
│  (Code/Repo)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 1: Input Processing (uml.py)      │
│  - Validate input                       │
│  - Auto-detect diagram types            │
│  - Route to appropriate handler         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 2: RAG Retrieval (uml_agent.py)   │
│  - Seed UML knowledge base (20 entries) │
│  - Semantic search for relevant context │
│  - Retrieve top 3 knowledge pieces      │
│  - Build context for LLM                │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 3: AI Analysis (Groq LLM)         │
│  - Model: llama-3.3-70b-versatile       │
│  - Inject RAG context                   │
│  - Generate Mermaid syntax              │
│  - Return structured JSON               │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Mermaid        │
│  Diagrams       │
└─────────────────┘
```

## Components

### 1. uml_rag_data.py
**Purpose**: UML knowledge base for RAG

**Content**: 20 knowledge entries covering:
- Class Diagram fundamentals
- Sequence Diagram patterns
- Flowchart best practices
- ERD conventions
- Language-specific patterns (Python, Java, JavaScript)
- Relationship detection strategies
- Mermaid syntax guidelines
- Design pattern visualization

### 2. uml_agent.py
**Purpose**: Core UML generation logic

**Key Methods**:
```python
seed_uml_knowledge()
    ├── Loads 20 knowledge entries
    ├── Creates vector embeddings
    └── Stores in ChromaDB

retrieve_uml_context(query, top_k=3)
    ├── Performs semantic search
    ├── Finds relevant knowledge
    └── Returns context with scores

detect_diagram_types(code, language)
    ├── Analyzes code patterns
    ├── Identifies suitable diagrams
    └── Returns diagram type list

generate_diagrams(code, language, types)
    ├── Retrieves RAG context
    ├── Calls LLM for each diagram type
    ├── Validates Mermaid syntax
    └── Returns diagram objects
```

### 3. uml.py (Router)
**Purpose**: FastAPI endpoints

**Endpoints**:
- `POST /api/generate-code-diagrams` - Generate diagrams
- `GET /api/uml/health` - Health check
- `GET /api/uml/diagram-types` - List supported types
- `POST /api/uml/detect-diagram-types` - Preview detection

## API Usage

### Generate Diagrams from Code

**Request**:
```bash
curl -X POST http://localhost:8000/api/generate-code-diagrams \
  -H "Content-Type: application/json" \
  -d '{
    "code": "class User:\n    def __init__(self):\n        pass",
    "language": "python",
    "diagram_types": ["auto"]
  }'
```

**Response**:
```json
{
  "diagrams": [
    {
      "type": "Class Diagram",
      "mermaid_code": "classDiagram\n    class User {\n        +__init__()\n    }",
      "description": "Class structure and relationships"
    }
  ],
  "analysis": "Generated 1 diagram(s) from code snippet",
  "diagram_count": 1
}
```

### Request Schema
```typescript
{
  code?: string,              // Source code (required if no repo_url)
  repository_url?: string,    // GitHub URL (coming soon)
  language: string,           // python, javascript, java, etc.
  diagram_types: string[]     // ["auto", "class", "sequence", etc.]
}
```

### Response Schema
```typescript
{
  diagrams: [
    {
      type: string,           // Diagram type name
      mermaid_code: string,   // Valid Mermaid syntax
      description: string     // What the diagram shows
    }
  ],
  analysis: string,           // Summary of generation
  diagram_count: number       // Number of diagrams
}
```

## RAG Knowledge Base

### Knowledge Categories

1. **Diagram Fundamentals** (5 entries)
   - Class diagrams
   - Sequence diagrams
   - Flowcharts
   - ERDs
   - State diagrams

2. **Language Patterns** (3 entries)
   - Python detection patterns
   - JavaScript/TypeScript patterns
   - Java detection patterns

3. **Advanced Techniques** (12 entries)
   - Relationship detection
   - Method call analysis
   - Control flow mapping
   - Database schema extraction
   - Design pattern visualization
   - Async/await patterns
   - Error handling representation
   - Multi-diagram strategies

### RAG Workflow

1. **Seeding**: Load 20 knowledge documents into ChromaDB
2. **Query**: User provides code to analyze
3. **Retrieval**: Semantic search finds top 3 relevant knowledge pieces
4. **Context**: Knowledge injected into LLM prompt
5. **Generation**: LLM uses context to generate accurate diagrams

## Testing

### Quick Test
```bash
cd FastApi
python test_uml_quick.py
```

### Expected Output
```
==================================================
UML DIAGRAM GENERATION TEST
==================================================

1. Detecting diagram types...
   Detected: ['class', 'sequence']

2. Generating UML diagrams...
   Generated 2 diagrams:

   Diagram 1: Class Diagram
   Description: Class structure and relationships
   
   Diagram 2: Sequence Diagram
   Description: Method call flow and interactions

✅ TEST PASSED - UML generation successful!
==================================================
```

### API Test with cURL
```bash
# Test health endpoint
curl http://localhost:8000/api/uml/health

# Test diagram generation
curl -X POST http://localhost:8000/api/generate-code-diagrams \
  -H "Content-Type: application/json" \
  -d '{
    "code": "class Car:\n    def drive(self):\n        pass",
    "language": "python",
    "diagram_types": ["class"]
  }'
```

## LLM Configuration

### Model Details
- **Model**: `llama-3.3-70b-versatile` (Groq)
- **Temperature**: 0.3 (consistent, focused output)
- **Max Tokens**: 2000 (sufficient for complex diagrams)
- **Response Format**: JSON (structured output)

### Prompt Structure
```
System: "You are an expert UML diagram generator..."

User Prompt:
├── Task description
├── RAG context (3 knowledge pieces)
├── Code to analyze
├── Requirements checklist
└── JSON output format specification
```

## Frontend Integration

The frontend component at `frontend/src/components/CodeToUmlDiagram.jsx` provides:
- Toggle between code and repository input
- Language selector
- Mermaid diagram rendering
- Interactive zoom controls
- SVG download
- Code view toggle

## Environment Variables

Required in `.env`:
```env
GROQ_API_KEY=your_groq_api_key
HF_API_KEY=your_huggingface_api_key  # For embeddings
```

## Limitations & Future Enhancements

### Current Limitations
- Repository analysis not yet implemented
- Maximum code length: ~4000 characters
- Single file analysis only
- English language knowledge base

### Planned Features
- ✅ Code snippet analysis (DONE)
- ⏳ GitHub repository cloning and analysis
- ⏳ Multi-file project analysis
- ⏳ Custom diagram styling
- ⏳ Diagram diff comparison
- ⏳ Export to PNG/PDF
- ⏳ Interactive diagram editing

## Error Handling

### Common Errors

1. **No Input Provided**
   ```json
   {
     "detail": "Either 'code' or 'repository_url' must be provided"
   }
   ```

2. **Invalid Mermaid Syntax**
   - LLM generates invalid syntax
   - Frontend fallback displays error message
   - User can view raw Mermaid code

3. **LLM API Failure**
   ```json
   {
     "detail": "Failed to generate diagrams: API timeout"
   }
   ```

## Performance

- **Code Analysis**: 3-8 seconds
- **RAG Retrieval**: <1 second
- **LLM Generation**: 2-5 seconds per diagram
- **Total Time**: 5-15 seconds for multiple diagrams

## Best Practices

### For Accurate Diagrams
1. Provide well-structured code with clear class/function definitions
2. Include type hints and comments
3. Use descriptive variable/method names
4. Keep code focused on single responsibility

### For Performance
1. Limit code length to ~2000 lines
2. Use specific diagram types instead of "auto"
3. Focus on core classes/functions only

## Troubleshooting

### Diagrams Not Generating
1. Check API key configuration
2. Verify code syntax is valid
3. Check FastAPI logs for errors
4. Test with sample code first

### Invalid Mermaid Syntax
1. View raw Mermaid code
2. Validate at https://mermaid.live
3. Report issue with code sample

### RAG Not Working
1. Check ChromaDB installation
2. Verify knowledge seeding completed
3. Check embeddings generation

## Contributing

To add new diagram types:
1. Add knowledge to `uml_rag_data.py`
2. Add detection logic to `detect_diagram_types()`
3. Update prompt in `_generate_single_diagram()`
4. Add to frontend diagram types list

## License

Part of the Mirai Hackathon project.
