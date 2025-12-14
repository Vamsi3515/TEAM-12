#!/usr/bin/env python3
"""
Test script for improved Experience Authenticity Agent with unlimited evidence support.

Tests:
1. Resume parsing from text
2. Evidence extraction from links
3. LLM-based claim verification
4. Multi-evidence support (GitHub, LeetCode, portfolio, etc.)
5. Proper JSON schema validation
"""

import asyncio
import json
from app.models.authenticity import (
    ResumeData,
    EvidenceItem,
    AuthenticityExtendedInput,
    AuthenticityExtendedOutput,
)
from app.core.Agents.authenticity_agent import analyze_authenticity


async def test_unlimited_evidence():
    """Test agent with unlimited evidence items."""
    
    # Create a realistic resume
    resume = ResumeData(
        full_name="Alice Johnson",
        skills=["Python", "FastAPI", "React", "JavaScript", "PostgreSQL", "Docker"],
        experience=[
            {
                "title": "Senior Backend Engineer",
                "company": "TechCorp",
                "duration": "2 years",
                "description": "Built microservices using FastAPI and Python"
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "duration": "1.5 years",
                "description": "Developed React frontend and Node.js backend"
            }
        ],
        projects=[
            {
                "name": "E-commerce Platform",
                "description": "Full-stack e-commerce with Python backend, React frontend, PostgreSQL"
            },
            {
                "name": "Real-time Chat App",
                "description": "WebSocket-based chat using FastAPI and React"
            }
        ],
        education=[
            {
                "degree": "BS Computer Science",
                "school": "State University",
                "year": 2020
            }
        ],
        certifications=["AWS Solutions Architect Associate", "Docker Certified Associate"],
        raw_text="Senior Backend Engineer at TechCorp (2021-2023). Built microservices with FastAPI. Full Stack Developer at StartupXYZ (2019-2021)..."
    )
    
    # Create unlimited evidence items
    evidences = [
        EvidenceItem(
            type="github_profile",
            url="https://github.com/alice-dev",
            title="GitHub Profile - alice-dev",
            metadata={"username": "alice-dev", "repos": 45, "stars": 120, "followers": 150}
        ),
        EvidenceItem(
            type="github_repo",
            url="https://github.com/alice-dev/ecommerce-platform",
            title="E-commerce Platform Repository",
            description="Full-stack e-commerce with Python, React, PostgreSQL",
            metadata={"stars": 45, "forks": 12, "language": "Python", "commits": 250}
        ),
        EvidenceItem(
            type="github_repo",
            url="https://github.com/alice-dev/realtime-chat",
            title="Real-time Chat Application",
            description="WebSocket-based chat using FastAPI and React",
            metadata={"stars": 23, "forks": 5, "language": "Python", "commits": 120}
        ),
        EvidenceItem(
            type="leetcode_profile",
            url="https://leetcode.com/alice-dev",
            title="LeetCode Profile",
            metadata={"username": "alice-dev", "problems_solved": 450, "contests": 28, "rating": 1850}
        ),
        EvidenceItem(
            type="portfolio",
            url="https://alice-portfolio.dev",
            title="Personal Portfolio",
            description="Showcase of projects and skills"
        ),
        EvidenceItem(
            type="blog",
            url="https://alice-dev-blog.medium.com",
            title="Technical Blog on Medium",
            description="Articles on FastAPI, React, and system design"
        ),
        EvidenceItem(
            type="certificate",
            url="https://aws.amazon.com/verification/alice-dev-cert-123",
            title="AWS Solutions Architect Associate",
            metadata={"issuer": "AWS", "credential_id": "ABC123XYZ", "issue_date": "2022-06", "expires": "2025-06"}
        ),
        EvidenceItem(
            type="kaggle",
            url="https://www.kaggle.com/alice-dev",
            title="Kaggle Profile",
            metadata={"competitions": 8, "datasets": 3}
        ),
    ]
    
    # Create extended input with unlimited evidence
    input_data = AuthenticityExtendedInput(
        resume=resume,
        evidences=evidences,
        additional_context="Candidate with strong backend and full-stack experience, active in open source and competitive programming."
    )
    
    print("=" * 80)
    print("TEST: Unlimited Evidence Support")
    print("=" * 80)
    print(f"\n📋 Resume: {resume.full_name}")
    print(f"🏆 Skills: {', '.join(resume.skills[:5])}... ({len(resume.skills)} total)")
    print(f"📚 Evidence Sources: {len(evidences)}")
    for i, ev in enumerate(evidences, 1):
        print(f"  {i}. {ev.type}: {ev.title}")
    
    print("\n⏳ Analyzing authenticity with improved agent...\n")
    
    try:
        result = await analyze_authenticity(input_data)
        
        # Validate response
        assert isinstance(result, AuthenticityExtendedOutput)
        assert 0 <= result.authenticity_score <= 100
        assert result.confidence_level in ["High", "Medium", "Low"]
        
        print("✅ TEST PASSED: Authenticity Analysis Complete")
        print("=" * 80)
        print(f"\n📊 Results Summary:")
        print(f"  Confidence Level: {result.confidence_level}")
        print(f"  Authenticity Score: {result.authenticity_score}/100")
        print(f"  Strong Evidence Items: {len(result.strong_evidence)}")
        print(f"  Risk Indicators: {len(result.risk_indicators)}")
        print(f"  Extracted Claims: {len(result.extracted_claims)}")
        print(f"  Claim Verifications: {len(result.claim_verifications)}")
        print(f"  Risk Flags: {len(result.risk_flags)}")
        print(f"  Missing Evidence: {len(result.missing_evidence)}")
        
        print(f"\n📈 Metrics:")
        for metric, value in (result.metrics or {}).items():
            print(f"  {metric}: {value:.2f}")
        
        print(f"\n✨ Overall Assessment:")
        print(f"  {result.overall_assessment}")
        
        print(f"\n💡 Top Improvement Suggestions:")
        for i, suggestion in enumerate(result.improvement_suggestions[:3], 1):
            print(f"  {i}. {suggestion}")
        
        print(f"\n⚠️  Risk Flags:")
        for flag in result.risk_flags[:2]:
            print(f"  - [{flag.severity.upper()}] {flag.code}: {flag.description}")
            if flag.remediation_step:
                print(f"    → {flag.remediation_step}")
        
        print("\n" + "=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_minimal_input():
    """Test agent with minimal input (no GitHub/LeetCode)."""
    
    resume = ResumeData(
        full_name="Bob Developer",
        skills=["Python", "JavaScript"],
        experience=[
            {
                "title": "Developer",
                "company": "Company",
                "duration": "1 year"
            }
        ],
        raw_text="Experienced Python and JavaScript developer"
    )
    
    input_data = AuthenticityExtendedInput(
        resume=resume,
        evidences=[],
        additional_context="Minimal profile without public evidence"
    )
    
    print("\n" + "=" * 80)
    print("TEST: Minimal Input (No External Evidence)")
    print("=" * 80)
    
    try:
        result = await analyze_authenticity(input_data)
        
        assert isinstance(result, AuthenticityExtendedOutput)
        assert 0 <= result.authenticity_score <= 100
        
        print("✅ TEST PASSED: Handles minimal input gracefully")
        print(f"  Confidence Level: {result.confidence_level}")
        print(f"  Authenticity Score: {result.authenticity_score}/100")
        print(f"  Assessment: {result.overall_assessment[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print("\n🚀 Starting Improved Authenticity Agent Tests...\n")
    
    results = []
    
    # Test 1: Unlimited evidence
    results.append(await test_unlimited_evidence())
    
    # Test 2: Minimal input
    results.append(await test_minimal_input())
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 TEST SUMMARY")
    print("=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"❌ {total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
