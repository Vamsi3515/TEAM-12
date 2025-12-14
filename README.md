# GenAI Multi-Agent Developer Intelligence Platform for Employability

A **GenAI-powered, multi-agent intelligence platform** that bridges the gap between **job rejections and real improvement**, helping **students, job seekers, recruiters, and hiring managers** make better, faster, and fairer decisions — all in one place.

---

## Problem Statement

Modern hiring is broken for **both candidates and recruiters**.

### Candidate Perspective (Students & Job Seekers)

Students and early-career developers struggle to understand their **true employability and engineering readiness** in today’s highly competitive job market.

They face repeated job rejections or interview failures, but rarely receive **clear, actionable feedback** on:

- Why their **resume was rejected** by ATS systems  
- Whether their **skills genuinely match job requirements**  
- How strong their **GitHub profile and real projects** actually are  
- Whether their **code quality and security** meet industry standards  
- How well they understand **system design and architecture**  
- What they should **learn next and in what order** to improve effectively  

As a result, candidates apply blindly, guess what to fix, and waste months preparing without clarity.

---

### Recruiter & Hiring Manager Perspective

Recruiters and hiring managers face a different but equally critical challenge:

- Overwhelming volumes of **low-quality or inflated resumes**
- Difficulty distinguishing **real skills from keyword stuffing**
- Limited visibility into **actual project depth, code quality, and authenticity**
- No scalable way to **explain rejections** or provide constructive feedback
- Significant interview bandwidth wasted on **misaligned candidates**

Most existing tools focus only on **filtering and rejecting**, not on **understanding or improving candidate quality**.

---

### The Core Gap

Current hiring and learning systems are **fragmented and one-sided**:

- ATS tools reject candidates but don’t explain *why*
- Resume tools ignore GitHub, code quality, and system design
- Code analysis tools don’t connect to hiring decisions
- Learning platforms are disconnected from real hiring signals

There is **no unified intelligence layer** that connects:

**rejection → evidence → skill gaps → improvement → re-evaluation**

---

## Our Solution

We built a **GenAI-powered multi-agent developer intelligence platform** that serves **both sides of the hiring ecosystem**.

Instead of isolated tools, our platform provides a **closed-loop employability system** where specialized AI agents work within a single unified flow to:

- Explain **job rejections** clearly and realistically  
- Validate **skill authenticity and project evidence**  
- Identify **skill gaps** and readiness issues  
- Guide candidates with **personalized learning paths**  
- Improve **code quality, security, and system design skills**  
- Help recruiters make **better-informed, evidence-backed decisions**

Each agent operates **independently**, but they are **orchestrated at the platform level** to deliver **end-to-end, actionable insights** — from diagnosis to improvement.

---

## AI Agents in the System

### 🔹 Super Agents (HR & Hiring Manager Focus)

#### 1. ATS Resume Analyzer & Rejection Feedback Agent
- Analyzes resumes against job roles and ATS criteria  
- Generates **realistic rejection reasons**
- Provides **clear, structured improvement feedback**
- Output is **email-ready**, similar to real recruiter responses  
- Helps recruiters explain rejections and helps candidates understand them  

#### 2. Experience Authenticity & Skill Consistency Agent
- Analyzes **consistency between resume claims and real evidence**
- Uses GitHub, code patterns, and optional coding platform signals
- Produces **confidence and risk indicators**, not accusations
- Highlights where skills are **strongly supported** or **weakly demonstrated**
- Helps recruiters reduce noise and helps candidates strengthen proof of skills  

---

### 🔹 Supporting Agents (Candidate Growth & Readiness)

#### 3. Skill Gap Analyzer
- Compares resume skills with target job requirements
- Identifies **missing or weak skills**
- Prioritizes what to learn first

#### 4. Learning Flow Generator
- Creates a **structured, personalized learning roadmap**
- Breaks learning into clear, achievable stages
- Focuses on practical, job-oriented progress

#### 5. UML Diagram Generator
- Converts natural language requirements into **UML system design diagrams**
- Helps candidates practice **architecture and design thinking**
- Useful for interviews, academics, and real projects

#### 6. Code Security Analyzer
- Analyzes code for **security vulnerabilities**
- Detects insecure coding practices (e.g., OWASP issues)
- Suggests **clear fixes and best practices**

#### 7. GitHub Repository Analyzer
- Evaluates GitHub profiles and repositories
- Checks structure, activity, documentation, and code quality
- Provides feedback on **industry readiness**

---

## How It Works (Simple Flow)

1. User provides resume, job role, GitHub link, or code  
2. Resume is analyzed and **rejection reasons are generated**
3. Skill authenticity and evidence consistency are evaluated
4. Skill gaps are identified for the target role
5. A **personalized learning roadmap** is generated
6. System design assistance via UML diagrams
7. Code and GitHub are analyzed for quality and security
8. User receives **clear, actionable feedback** to improve and reapply confidently  

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
- Vector Search
- Prompt Engineering