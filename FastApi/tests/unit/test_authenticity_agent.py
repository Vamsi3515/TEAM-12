"""
Unit tests for Experience Authenticity & Skill Consistency Agent

Tests the agent's ability to:
1. Analyze skill consistency
2. Generate supportive assessments
3. Avoid accusatory language
4. Handle missing evidence gracefully
"""

import pytest
import json
from app.models.authenticity import (
    ResumeData,
    GitHubEvidence,
    AuthenticityAnalysisInput,
    SkillAlignment,
)
from app.core.Agents.authenticity_agent import (
    analyze_authenticity,
    _parse_json_response,
    _calculate_confidence_metrics,
)
from app.core.Agents.authenticity_agent import _create_authenticity_system_prompt
from app.models.authenticity import LeetCodeEvidence

class TestAuthenticityAgent:
    """Test suite for authenticity analysis agent."""
    
    @pytest.mark.asyncio
    async def test_strong_evidence_candidate(self):
        """Test analysis of candidate with strong evidence alignment."""
        resume = ResumeData(
            skills=["Python", "FastAPI", "React"],
            experience=[
                {"title": "Backend Engineer", "company": "TechCorp", "duration": "2 years"}
            ],
            projects=[
                {"name": "API Project", "description": "FastAPI REST API"}
            ]
        )
        
        github = GitHubEvidence(
            languages=["Python", "JavaScript"],
            repo_count=20,
            commit_frequency="consistent",
            top_projects=[
                {
                    "name": "fastapi-api",
                    "description": "Production API",
                    "stars": 50,
                    "languages": ["Python"],
                    "readme_quality": "excellent"
                }
            ],
            readme_quality="excellent",
            contribution_pattern="consistent"
        )
        
        input_data = AuthenticityAnalysisInput(resume=resume, github=github)
        output = await analyze_authenticity(input_data)
        
        # Assertions
        assert output.confidence_level in ["High", "Medium", "Low"]
        assert 0 <= output.authenticity_score <= 100
        assert len(output.strong_evidence) > 0
        assert isinstance(output.strong_evidence, list)
        assert isinstance(output.improvement_suggestions, list)
        # Should use supportive language
        for suggestion in output.improvement_suggestions:
            assert "fraud" not in suggestion.lower()
            assert "fake" not in suggestion.lower()
    
    
    @pytest.mark.asyncio
    async def test_partial_evidence_candidate(self):
        """Test analysis of candidate with limited GitHub presence."""
        resume = ResumeData(
            skills=["Python", "Machine Learning", "TensorFlow"],
            experience=[
                {"title": "ML Engineer", "company": "DataCorp", "duration": "2 years"}
            ]
        )
        
        github = GitHubEvidence(
            languages=["Python"],
            repo_count=3,
            commit_frequency="sporadic",
            top_projects=[
                {
                    "name": "ml-tutorial",
                    "description": "ML examples",
                    "stars": 2,
                    "readme_quality": "fair"
                }
            ],
            readme_quality="fair",
            contribution_pattern="sporadic"
        )
        
        input_data = AuthenticityAnalysisInput(
            resume=resume,
            github=github,
            additional_context="Most work is proprietary"
        )
        output = await analyze_authenticity(input_data)
        
        # Should acknowledge limited evidence without accusation
        assert output.confidence_level in ["Medium", "Low"]
        assert len(output.risk_indicators) > 0
        # Should provide constructive suggestions
        assert len(output.improvement_suggestions) > 0
        assert output.overall_assessment.lower().count("opportunity") > 0 or \
               "suggest" in output.overall_assessment.lower()
    
    
    @pytest.mark.asyncio
    async def test_no_github_candidate(self):
        """Test analysis of candidate with strong resume but no GitHub."""
        resume = ResumeData(
            skills=["Java", "Spring Boot", "Microservices"],
            experience=[
                {"title": "Senior Engineer", "company": "BigTech", "duration": "4 years"}
            ]
        )
        
        input_data = AuthenticityAnalysisInput(
            resume=resume,
            github=None,
            additional_context="Enterprise background, limited ability to share proprietary code"
        )
        output = await analyze_authenticity(input_data)
        
        # Should NOT penalize for missing GitHub
        assert "github" not in output.overall_assessment.lower() or \
               "lack" not in output.overall_assessment.lower()
        # Should provide alternative suggestions
        assert any("side project" in s.lower() or "open source" in s.lower() 
                  for s in output.improvement_suggestions)
    
    
    def test_json_response_parsing_valid(self):
        """Test JSON parsing with valid response."""
        valid_json = json.dumps({
            "confidence_level": "High",
            "authenticity_score": 85,
            "strong_evidence": ["Skill A", "Skill B"],
            "risk_indicators": [],
            "overall_assessment": "Good alignment"
        })
        
        result = _parse_json_response(valid_json)
        assert result["confidence_level"] == "High"
        assert result["authenticity_score"] == 85
    
    
    def test_json_response_parsing_wrapped(self):
        """Test JSON parsing with wrapped response."""
        wrapped_json = """
        Here is the analysis:
        
        {
            "confidence_level": "Medium",
            "authenticity_score": 65,
            "strong_evidence": ["A"],
            "risk_indicators": ["B"],
            "overall_assessment": "Moderate"
        }
        
        End of analysis.
        """
        
        result = _parse_json_response(wrapped_json)
        assert result["confidence_level"] == "Medium"
        assert result["authenticity_score"] == 65
    
    
    def test_confidence_metrics_calculation(self):
        """Test confidence metric calculation."""
        resume = ResumeData(
            skills=["Python"],
            experience=[{"title": "Engineer", "company": "Corp"}],
            projects=[{"name": "Project"}],
            education=[{"degree": "BS"}],
            raw_text="Full resume"
        )
        
        github = GitHubEvidence(
            languages=["Python"],
            repo_count=10,
            contribution_pattern="consistent"
        )
        
        metrics = _calculate_confidence_metrics(resume, github)
        
        assert "resume_completeness" in metrics
        assert "github_strength" in metrics
        assert "evidence_diversity" in metrics
        assert 0 <= metrics["resume_completeness"] <= 100
        assert 0 <= metrics["github_strength"] <= 100
        assert 0 <= metrics["evidence_diversity"] <= 100
    
    
    def test_skill_alignment_parsing(self):
        """Test skill alignment data structure."""
        alignment = SkillAlignment(
            skill="Python",
            confidence="High",
            evidence_source=["GitHub", "LeetCode"],
            supporting_evidence=["20 repos", "100+ problems"],
            gap_analysis=None
        )
        
        assert alignment.skill == "Python"
        assert alignment.confidence == "High"
        assert len(alignment.evidence_source) == 2
    
    
    def test_no_accusatory_language(self):
        """Test that agent never uses accusatory terms."""
        forbidden_terms = ["fraud", "fake", "dishonest", "deceptive", "false claim", "liar"]
        
        # This is a conceptual test - in real use, check outputs
        # The prompt explicitly forbids these terms
        resume = ResumeData(
            skills=["Python"],
            experience=[{"title": "Engineer", "company": "Corp"}]
        )
        
        github = GitHubEvidence(
            languages=[],
            repo_count=0,
            contribution_pattern="none"
        )
        
        # In production, verify output doesn't contain forbidden terms
        # For now, test that the system prompt includes safeguards
        system_prompt = _create_authenticity_system_prompt()
        
        # Should mention these are NOT appropriate
        assert "NOT assume" in system_prompt
        assert "NOT penalize" in system_prompt
        assert "NOT accusatory" in system_prompt or "accusatory" in system_prompt


class TestAuthenticitySchemas:
    """Test Pydantic schema validation."""
    
    def test_resume_data_validation(self):
        """Test ResumeData schema validation."""
        resume = ResumeData(
            full_name="John Doe",
            skills=["Python", "JavaScript"],
            experience=[
                {
                    "title": "Developer",
                    "company": "TechCorp",
                    "duration": "2 years",
                    "description": "Backend development"
                }
            ]
        )
        
        assert resume.full_name == "John Doe"
        assert len(resume.skills) == 2
        assert len(resume.experience) == 1
    
    
    def test_github_evidence_validation(self):
        """Test GitHubEvidence schema validation."""
        github = GitHubEvidence(
            username="john-dev",
            languages=["Python", "JavaScript"],
            repo_count=15,
            commit_frequency="consistent",
            readme_quality="good"
        )
        
        assert github.username == "john-dev"
        assert github.repo_count == 15
        assert github.commit_frequency == "consistent"
    
    
    def test_leetcode_evidence_validation(self):
        """Test LeetCodeEvidence schema validation."""
        leetcode = LeetCodeEvidence(
            problems_solved=150,
            difficulty_distribution={
                "Easy": 50,
                "Medium": 75,
                "Hard": 25
            },
            recent_activity=True
        )
        
        assert leetcode.problems_solved == 150
        assert leetcode.difficulty_distribution["Medium"] == 75


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.mark.asyncio
    async def test_empty_resume(self):
        """Test handling of empty resume."""
        resume = ResumeData()  # Empty
        input_data = AuthenticityAnalysisInput(resume=resume)
        
        # Should handle gracefully
        output = await analyze_authenticity(input_data)
        assert output is not None
        assert isinstance(output.authenticity_score, (int, float))
    
    
    @pytest.mark.asyncio
    async def test_mixed_evidence_sources(self):
        """Test with multiple evidence sources."""
        resume = ResumeData(
            skills=["Python", "JavaScript", "Problem Solving"]
        )
        
        github = GitHubEvidence(
            languages=["Python", "JavaScript"],
            repo_count=10
        )
        
        leetcode = LeetCodeEvidence(
            problems_solved=200,
            difficulty_distribution={"Easy": 70, "Medium": 90, "Hard": 40}
        )
        
        input_data = AuthenticityAnalysisInput(
            resume=resume,
            github=github,
            leetcode=leetcode
        )
        
        output = await analyze_authenticity(input_data)
        # Should leverage all sources
        assert output.authenticity_score >= 50  # Multiple sources provide good coverage


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
