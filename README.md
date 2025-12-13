# GenAI Multi-Agent Developer Intelligence Platform for Employability

A GenAI-powered, multi-agent platform that explains job rejections and helps students and early-career developers improve resumes, skills, system design, code security, and GitHub quality — all in one place.
---

## Problem Statement

Students and early-career developers struggle to understand their overall **employability and engineering readiness** in today’s highly competitive job market.

Many face repeated job rejections or poor interview outcomes, but they lack **clear, actionable, end-to-end feedback** on:

- Whether their **resume and skills** truly match job requirements  
- How strong their **GitHub profile and projects** actually are  
- Whether their **code quality and security** meet industry standards  
- How well they understand **system design and architecture**  
- What they should **learn next and in what order** to improve effectively  

While many tools exist, they are **fragmented and isolated**:

- Resume tools don’t analyze code or GitHub  
- Learning platforms don’t explain rejection reasons  
- Code analysis tools don’t connect to career readiness  
- System design practice lacks real feedback loops  

As a result, candidates receive **partial insights**, apply blindly, and struggle to convert effort into **real improvement and job readiness**.


---

## Our Solution

We built a **GenAI-powered multi-agent platform** where specialized AI agents address different aspects of **developer employability** within a single, unified system.

Instead of providing isolated or disconnected feedback, the platform:

- Explains **job rejection reasons** and resume-related issues  
- Identifies **skill gaps** based on target role requirements  
- Generates **personalized learning flows** and improvement paths  
- Analyzes **code quality, security, and best practices**  
- Converts natural language requirements into **UML system design diagrams**  
- Evaluates **GitHub profile strength** and project readiness  

Each agent operates **independently**, but they are **orchestrated at the platform level**, allowing users to receive **end-to-end, actionable insights** in one continuous flow — from diagnosis to improvement.

---

## AI Agents in the System

### 1. ATS Resume Analyzer & Rejection Feedback Agent
- Analyzes resumes against job roles
- Generates **realistic rejection reasons**
- Provides **clear improvement feedback**
- Output is **email-ready**, similar to real recruiter responses

### 2. Skill Gap Analyzer
- Compares resume skills with the target job role
- Identifies **missing or weak skills**
- Prioritizes what to learn first

### 3. Learning Flow Generator
- Creates a **structured, personalized learning roadmap**
- Breaks learning into **clear steps**
- Focuses on practical, job-oriented progress

### 4. UML Diagram Generator
- Converts natural language requirements into **system design UML diagrams**
- Helps candidates practice **architecture and design thinking**

### 5. Code Security Analyzer
- Analyzes code for **security vulnerabilities**
- Detects insecure coding practices
- Suggests **clear fixes and improvements**

### 6. GitHub Repository Analyzer
- Evaluates GitHub profile and repositories
- Checks structure, activity, and code quality
- Gives feedback on **industry readiness**

---

## How It Works (Simple Flow)

1. User uploads resume / job role / code / GitHub link  
2. Resume is analyzed and **rejection reasons are generated**
3. Skill gaps are identified for the target role
4. A **personalized learning roadmap** is created
5. System design help via UML diagrams
6. Code and GitHub are analyzed for quality and security
7. User gets **clear, actionable feedback** to improve and reapply confidently

---

## Tech Stack

### Backend
- **FastAPI**
- **Python**

### AI / LLM
- **Groq**
- **Gemini** (optional fallback)
- **HuggingFace Models**

### GenAI Techniques
- Retrieval-Augmented Generation (RAG)
- Embeddings
- Vector Database
- Prompt Engineering
- Grounded Generation

### Database / Storage
- Vector DB (Chroma or similar)

### Frontend
- **React**

---

## Grounding & Reliability

To reduce hallucinations and improve reliability:
- Uses **RAG** with real resume, code, and GitHub inputs
- Applies **grounded generation** instead of free-form answers
- Uses static analysis for code and structured output formats
- Lightweight validation checks for consistent responses

---

## Why This Is Useful (Impact)

This platform helps students and job seekers:
- Understand **why they are getting rejected**
- Stop guessing and start **improving with clarity**
- Learn the **right skills in the right order**
- Improve resumes, GitHub, code quality, and design skills
- Become **job-ready faster and with confidence**

Instead of multiple disconnected tools, they get **one clear path forward**.
