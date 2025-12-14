"""
Example: How to use the Experience Authenticity & Skill Consistency Agent

This demonstrates the agent with sample data and shows expected outputs.
"""

import json
from app.models.authenticity import (
    ResumeData,
    GitHubEvidence,
    LeetCodeEvidence,
    AuthenticityAnalysisInput,
)

# ==================== EXAMPLE 1: Strong Evidence Candidate ====================

def create_example_strong_candidate():
    """Example: Candidate with strong GitHub evidence supporting resume claims."""
    
    resume = ResumeData(
        full_name="Alice Johnson",
        skills=["Python", "FastAPI", "PostgreSQL", "React", "Docker", "AWS"],
        experience=[
            {
                "title": "Backend Engineer",
                "company": "TechCorp",
                "duration": "2 years",
                "description": "Developed FastAPI microservices"
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "duration": "1.5 years",
                "description": "Built React + Python applications"
            }
        ],
        projects=[
            {
                "name": "E-commerce API",
                "description": "Built a full-featured e-commerce backend with FastAPI"
            },
            {
                "name": "Task Management App",
                "description": "React + Node.js full-stack project"
            }
        ],
        education=[
            {
                "degree": "BS Computer Science",
                "school": "State University",
                "year": 2021
            }
        ],
        certifications=["AWS Solutions Architect Associate"],
    )
    
    github = GitHubEvidence(
        username="alice-johdev",
        languages=["Python", "JavaScript", "SQL", "Dockerfile"],
        repo_count=28,
        commit_frequency="consistent",  # Multiple commits per week
        top_projects=[
            {
                "name": "ecommerce-api",
                "description": "Production-grade FastAPI REST API with PostgreSQL",
                "stars": 45,
                "languages": ["Python"],
                "updated": "1 week ago",
                "readme_quality": "excellent"
            },
            {
                "name": "task-manager",
                "description": "Full-stack React + Python task management",
                "stars": 28,
                "languages": ["Python", "JavaScript"],
                "updated": "2 weeks ago",
                "readme_quality": "good"
            },
            {
                "name": "docker-deployment",
                "description": "Docker + Kubernetes examples for microservices",
                "stars": 12,
                "languages": ["Dockerfile", "Bash"],
                "updated": "1 month ago",
                "readme_quality": "good"
            }
        ],
        readme_quality="excellent",
        contribution_pattern="consistent",
    )
    
    leetcode = LeetCodeEvidence(
        problems_solved=187,
        difficulty_distribution={
            "Easy": 65,
            "Medium": 89,
            "Hard": 33
        },
        recent_activity=True,
    )
    
    return AuthenticityAnalysisInput(
        resume=resume,
        github=github,
        leetcode=leetcode,
    )


# ==================== EXAMPLE 2: Partial Evidence Candidate ====================

def create_example_partial_candidate():
    """Example: Candidate with resume claims but limited GitHub evidence."""
    
    resume = ResumeData(
        full_name="Bob Smith",
        skills=["Python", "Machine Learning", "TensorFlow", "Data Analysis", "SQL"],
        experience=[
            {
                "title": "ML Engineer",
                "company": "DataCo",
                "duration": "2 years",
                "description": "Developed ML models for recommendations"
            },
            {
                "title": "Data Analyst",
                "company": "RetailCorp",
                "duration": "1 year",
                "description": "SQL-based analysis and reporting"
            }
        ],
        projects=[
            {
                "name": "Recommendation Engine",
                "description": "TensorFlow-based collaborative filtering model"
            },
            {
                "name": "Fraud Detection System",
                "description": "ML model for transaction fraud detection"
            }
        ],
        education=[
            {
                "degree": "MS Data Science",
                "school": "Tech University",
                "year": 2022
            }
        ],
    )
    
    github = GitHubEvidence(
        username="bob-ml-dev",
        languages=["Python", "Jupyter"],
        repo_count=5,
        commit_frequency="sporadic",  # 1-2 commits per month
        top_projects=[
            {
                "name": "ml-examples",
                "description": "Tutorial notebooks on ML",
                "stars": 3,
                "languages": ["Jupyter"],
                "updated": "6 months ago",
                "readme_quality": "fair"
            },
            {
                "name": "data-analysis-scripts",
                "description": "Various Python scripts for data processing",
                "stars": 1,
                "languages": ["Python"],
                "updated": "1 year ago",
                "readme_quality": "poor"
            }
        ],
        readme_quality="fair",
        contribution_pattern="sporadic",
    )
    
    return AuthenticityAnalysisInput(
        resume=resume,
        github=github,
        additional_context="Most work has been proprietary at previous companies. Looking to build more public portfolio."
    )


# ==================== EXAMPLE 3: No GitHub Candidate ====================

def create_example_no_github_candidate():
    """Example: Candidate with strong resume but no GitHub presence."""
    
    resume = ResumeData(
        full_name="Carol Lee",
        skills=["Java", "Spring Boot", "Microservices", "AWS", "Kubernetes"],
        experience=[
            {
                "title": "Senior Software Engineer",
                "company": "BigTech Corp",
                "duration": "4 years",
                "description": "Led backend services architecture and team"
            },
            {
                "title": "Backend Developer",
                "company": "FinanceStart",
                "duration": "2 years",
                "description": "Developed financial transaction systems"
            }
        ],
        projects=[
            {
                "name": "Microservices Migration",
                "description": "Migrated monolith to microservices architecture"
            },
            {
                "name": "Payment Processing System",
                "description": "Real-time payment gateway with Kubernetes"
            }
        ],
        education=[
            {
                "degree": "BS Computer Engineering",
                "school": "Engineering Institute",
                "year": 2018
            }
        ],
        certifications=["AWS Solutions Architect", "Kubernetes Administrator"],
        raw_text="Career in large corporate settings with emphasis on closed-source enterprise systems."
    )
    
    return AuthenticityAnalysisInput(
        resume=resume,
        github=None,  # No GitHub provided
        additional_context="Worked in regulated financial sector with proprietary codebase. Limited ability to showcase public work. Looking to transition to startups with open-source culture."
    )


# ==================== EXPECTED OUTPUT EXAMPLES ====================

EXPECTED_OUTPUT_STRONG_CANDIDATE = {
    "confidence_level": "High",
    "authenticity_score": 88,
    "strong_evidence": [
        "Python expertise clearly demonstrated: 28 GitHub repos with consistent commits, 45 stars on e-commerce API",
        "FastAPI mastery evident: Production-grade API with excellent documentation and architecture",
        "Full-stack capabilities shown: React + Python projects with solid execution",
        "Strong problem-solving skills: 187 LeetCode problems solved (89 Medium, 33 Hard)",
        "DevOps knowledge: Docker/Kubernetes projects with good documentation",
        "Consistent learning: Regular GitHub activity, recent commits across projects"
    ],
    "risk_indicators": [
        "Limited AI/ML project visibility (if that's a claimed specialty)",
        "Could strengthen AWS expertise with more Infrastructure-as-Code examples"
    ],
    "overall_assessment": "Excellent alignment between resume claims and GitHub evidence. Strong track record of shipping production-grade systems with consistent contributions. Demonstrates both technical depth and breadth through diverse, well-documented projects.",
    "improvement_suggestions": [
        "Consider adding AWS infrastructure projects to portfolio (IaC, Lambda, etc.)",
        "Document project architecture decisions in READMEs for better clarity",
        "Maintain consistent commit patterns to continue demonstrating active learning"
    ]
}

EXPECTED_OUTPUT_PARTIAL_CANDIDATE = {
    "confidence_level": "Medium",
    "authenticity_score": 58,
    "strong_evidence": [
        "Data Science foundation solid: MS in Data Science from respected program",
        "Python skills evident from available projects",
        "Experience claims supported by work history timeline"
    ],
    "risk_indicators": [
        "Limited public ML/TensorFlow projects - claimed specialization not visible in GitHub",
        "Sporadic contribution pattern could suggest limited open-source engagement",
        "READMEs could be more detailed - documentation quality is fair",
        "Recommendation system and fraud detection projects mentioned in resume not visible in GitHub"
    ],
    "overall_assessment": "Resume shows strong background, but GitHub presence doesn't fully demonstrate claimed ML specializations. This is common in proprietary environments, but building public projects would strengthen candidacy significantly.",
    "improvement_suggestions": [
        "Build 1-2 public ML projects (e.g., recommendation system, fraud detector) to showcase hands-on skills",
        "Share Kaggle competitions or Jupyter notebooks demonstrating model development",
        "Create detailed project READMEs explaining methodology, data processing, model evaluation",
        "Contribute to open-source ML projects (scikit-learn, TensorFlow, etc.)",
        "Document your Data Science work with clear explanations - employers want to see your thinking"
    ]
}

EXPECTED_OUTPUT_NO_GITHUB_CANDIDATE = {
    "confidence_level": "Medium",
    "authenticity_score": 72,
    "strong_evidence": [
        "Strong corporate experience: 4+ years at respected companies",
        "Relevant certifications: AWS Solutions Architect and Kubernetes Administrator",
        "Senior-level responsibilities: Led architecture and team at BigTech",
        "Experience with modern tech stack: Microservices, Kubernetes, AWS"
    ],
    "risk_indicators": [
        "No GitHub profile provided - limited ability to see hands-on coding",
        "Enterprise background means less opportunity to demonstrate with public code",
        "Skills like system design are harder to evaluate without visible projects"
    ],
    "overall_assessment": "Strong resume and certifications support claimed expertise. Enterprise background explains lack of GitHub presence. Transitioning to startup culture will benefit from demonstrating ability to build in more open environments.",
    "improvement_suggestions": [
        "Build 1-2 side projects showcasing microservices architecture (REST API, Docker setup)",
        "Create a GitHub profile with example Kubernetes configurations or Infrastructure-as-Code",
        "Share architecture decision documents or technical blog posts",
        "Contribute to open-source Kubernetes or distributed systems projects",
        "Document your past work at high level - show architectural thinking even if code is proprietary"
    ]
}


if __name__ == "__main__":
    print("=" * 80)
    print("EXAMPLE 1: Strong Evidence Candidate")
    print("=" * 80)
    example1 = create_example_strong_candidate()
    print(json.dumps(example1.model_dump(), indent=2))
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Partial Evidence Candidate")
    print("=" * 80)
    example2 = create_example_partial_candidate()
    print(json.dumps(example2.model_dump(), indent=2))
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: No GitHub Candidate")
    print("=" * 80)
    example3 = create_example_no_github_candidate()
    print(json.dumps(example3.model_dump(), indent=2))
