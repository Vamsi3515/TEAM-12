"""Pytest-based evaluation suite for AI agents.

This module runs comprehensive evaluations on ATS and GitHub agents,
comparing their outputs against expected results from test fixtures.
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any
import pytest

from app.core.Agents.ats_agent import analyze_ats
from app.core.Agents.github_agent import analyze_github_repo
from app.core.Agents.authenticity_agent import analyze_authenticity
from app.models.authenticity import (
    ResumeData,
    GitHubEvidence,
    LeetCodeEvidence,
    AuthenticityExtendedInput
)
from app.core.Utils.eval_metrics import (
    score_accuracy,
    keyword_overlap,
    substring_match,
    json_structure_validity,
    response_time_check,
    aggregate_metrics
)


# Test configuration
FIXTURES_DIR = Path(__file__).parent / "fixtures"
ATS_FIXTURES = FIXTURES_DIR / "ats_test_cases.json"
GITHUB_FIXTURES = FIXTURES_DIR / "github_test_cases.json"
AUTHENTICITY_FIXTURES = FIXTURES_DIR / "authenticity_test_cases.json"
LEARNING_FIXTURES = FIXTURES_DIR / "learning_flow_test_cases.json"
RESPONSE_TIME_THRESHOLD_MS = 30000  # 30 seconds


# Load test cases
def load_test_cases(fixture_file: Path) -> List[Dict[str, Any]]:
    """Load test cases from JSON fixture file."""
    with open(fixture_file, 'r', encoding='utf-8') as f:
        return json.load(f)


# ATS Agent Tests
class TestATSAgent:
    """Test suite for ATS analysis agent."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_idx", range(16))  # Run all 16 test cases
    async def test_ats_analysis(self, test_idx, record_property):
        """Test ATS analysis against expected outputs."""
        ats_test_cases = load_test_cases(ATS_FIXTURES)
        
        if test_idx >= len(ats_test_cases):
            pytest.skip(f"Test case {test_idx} not found")
        
        test_case = ats_test_cases[test_idx]
        test_name = test_case["test_case_name"]
        
        # Record test name for reporting
        record_property("test_case_name", test_name)
        record_property("description", test_case["description"])
        
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"Description: {test_case['description']}")
        print(f"{'='*60}")
        
        # Measure response time
        start_time = time.time()
        
        # Run ATS analysis
        result = await analyze_ats(
            resume_text=test_case["resume_text"],
            job_description=test_case.get("job_description"),
            email=None  # Don't send emails during tests
        )
        
        duration_ms = (time.time() - start_time) * 1000
        record_property("duration_ms", duration_ms)
        
        # Convert result to dict for easier testing
        result_dict = {
            "ats_score": result.ats_score,
            "rejection_reasons": result.rejection_reasons,
            "strengths": result.strengths,
            "issues": result.issues,
            "actionable_suggestions": result.actionable_suggestions,
            "summary": result.summary
        }
        
        # Collect all metrics
        metrics = {}
        
        # 1. Test score accuracy
        expected_range = test_case["expected_score_range"]
        score_metric = score_accuracy(
            result.ats_score,
            expected_range["min"],
            expected_range["max"]
        )
        metrics["score_accuracy"] = score_metric
        record_property("score_accuracy", score_metric['accuracy'])
        record_property("actual_score", result.ats_score)
        record_property("expected_min", expected_range["min"])
        record_property("expected_max", expected_range["max"])
        print(f"\n✓ Score: {result.ats_score} (expected {expected_range['min']}-{expected_range['max']})")
        print(f"  Accuracy: {score_metric['accuracy']:.2%}")
        
        # 2. Test rejection reasons
        if test_case["expected_rejection_reasons"]:
            rejection_metric = substring_match(
                result.rejection_reasons,
                test_case["expected_rejection_reasons"]
            )
            metrics["rejection_reasons"] = rejection_metric
            record_property("rejection_reasons_match", rejection_metric['match_rate'])
            print(f"\n✓ Rejection Reasons Match: {rejection_metric['match_rate']:.2%}")
            if rejection_metric["missing"]:
                print(f"  Missing: {rejection_metric['missing']}")
        
        # 3. Test strengths
        if test_case["expected_strengths"]:
            strengths_metric = substring_match(
                result.strengths,
                test_case["expected_strengths"]
            )
            metrics["strengths"] = strengths_metric
            record_property("strengths_match", strengths_metric['match_rate'])
            print(f"\n✓ Strengths Match: {strengths_metric['match_rate']:.2%}")
            if strengths_metric["missing"]:
                print(f"  Missing: {strengths_metric['missing']}")
        
        # 4. Test issues
        if test_case.get("expected_issues"):
            issues_metric = substring_match(
                result.issues,
                test_case["expected_issues"]
            )
            metrics["issues"] = issues_metric
            record_property("issues_match", issues_metric['match_rate'])
            print(f"\n✓ Issues Match: {issues_metric['match_rate']:.2%}")
        
        # 5. Test suggestions
        if test_case.get("expected_suggestions"):
            suggestions_metric = substring_match(
                result.actionable_suggestions,
                test_case["expected_suggestions"]
            )
            metrics["suggestions"] = suggestions_metric
            record_property("suggestions_match", suggestions_metric['match_rate'])
            print(f"\n✓ Suggestions Match: {suggestions_metric['match_rate']:.2%}")
        
        # 6. Test JSON structure
        structure_metric = json_structure_validity(
            result_dict,
            required_fields=[
                "ats_score",
                "rejection_reasons",
                "strengths",
                "issues",
                "actionable_suggestions",
                "summary"
            ]
        )
        metrics["structure"] = structure_metric
        record_property("structure_valid", structure_metric['valid'])
        print(f"\n✓ Structure Valid: {structure_metric['valid']}")
        
        # 7. Test response time
        time_metric = response_time_check(duration_ms, RESPONSE_TIME_THRESHOLD_MS)
        metrics["response_time"] = time_metric
        record_property("response_time_ok", time_metric['passed'])
        print(f"\n✓ Response Time: {duration_ms:.0f}ms (threshold: {RESPONSE_TIME_THRESHOLD_MS}ms)")
        
        # Store metrics for reporting
        test_case["_metrics"] = metrics
        test_case["_duration_ms"] = duration_ms
        test_case["_result"] = result_dict
        
        # Calculate overall pass/fail
        # Test passes if score is accurate and structure is valid
        assert score_metric["passed"], f"Score {result.ats_score} not in expected range {expected_range}"
        assert structure_metric["valid"], f"Invalid structure: {structure_metric['missing_required']}"
        
        print(f"\n✅ Test '{test_name}' PASSED")


# GitHub Agent Tests
class TestGitHubAgent:
    """Test suite for GitHub analysis agent."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_idx", range(len(load_test_cases(GITHUB_FIXTURES))))  # Run all GitHub fixture cases
    async def test_github_analysis(self, test_idx):
        """Test GitHub analysis against expected outputs."""
        github_test_cases = load_test_cases(GITHUB_FIXTURES)
        
        if test_idx >= len(github_test_cases):
            pytest.skip(f"Test case {test_idx} not found")
        
        test_case = github_test_cases[test_idx]
        test_name = test_case["test_case_name"]
        
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"Description: {test_case['description']}")
        print(f"Repo: {test_case['repo_url']}")
        print(f"{'='*60}")
        
        # Measure response time
        start_time = time.time()
        
        try:
            # Run GitHub analysis
            result = await analyze_github_repo(test_case["repo_url"])
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Collect metrics
            metrics = {}
            
            # 1. Test tech stack detection
            if test_case["expected_tech_stack"]:
                tech_stack_metric = substring_match(
                    result.tech_stack,
                    test_case["expected_tech_stack"]
                )
                metrics["tech_stack"] = tech_stack_metric
                print(f"\n✓ Tech Stack Match: {tech_stack_metric['match_rate']:.2%}")
                print(f"  Detected: {result.tech_stack[:5]}")  # Show first 5
            
            # 2. Test metrics ranges
            metrics_ranges = test_case["expected_metrics_ranges"]
            metric_scores = {}
            
            for metric in result.metrics:
                metric_name = metric.name.lower().replace(" ", "_")
                if metric_name in metrics_ranges:
                    expected = metrics_ranges[metric_name]
                    score_metric = score_accuracy(
                        metric.score,
                        expected["min"],
                        expected["max"]
                    )
                    metric_scores[metric_name] = score_metric
                    print(f"\n✓ {metric.name}: {metric.score:.1f} (expected {expected['min']}-{expected['max']})")
            
            metrics["metric_scores"] = metric_scores
            
            # 3. Test strengths
            if test_case["expected_strengths"]:
                strengths_metric = substring_match(
                    result.strengths,
                    test_case["expected_strengths"]
                )
                metrics["strengths"] = strengths_metric
                print(f"\n✓ Strengths Match: {strengths_metric['match_rate']:.2%}")
            
            # 4. Test weaknesses
            if test_case["expected_weaknesses"]:
                weaknesses_metric = substring_match(
                    result.weaknesses,
                    test_case["expected_weaknesses"]
                )
                metrics["weaknesses"] = weaknesses_metric
                print(f"\n✓ Weaknesses Match: {weaknesses_metric['match_rate']:.2%}")
            
            # 5. Test response time
            time_metric = response_time_check(duration_ms, RESPONSE_TIME_THRESHOLD_MS)
            metrics["response_time"] = time_metric
            print(f"\n✓ Response Time: {duration_ms:.0f}ms")
            
            # Store results
            test_case["_metrics"] = metrics
            test_case["_duration_ms"] = duration_ms
            
            # Basic assertions
            assert result.tech_stack is not None, "Tech stack should not be None"
            assert result.metrics, "Metrics should not be empty"
            assert result.repo_summary, "Summary should not be empty"
            
            print(f"\n✅ Test '{test_name}' PASSED")
            
        except Exception as e:
            print(f"\n❌ Test '{test_name}' FAILED: {str(e)}")
            # Don't fail on API errors (rate limits, network issues)
            if "rate limit" in str(e).lower() or "403" in str(e):
                pytest.skip(f"Skipping due to API limitation: {e}")
            raise


# Security Agent Tests
class TestSecurityAgent:
    """Test suite for Security analyzer."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_idx", range(len(load_test_cases(Path(__file__).parent / "fixtures" / "security_test_cases.json"))))
    async def test_security_analysis(self, test_idx):
        security_cases = load_test_cases(Path(__file__).parent / "fixtures" / "security_test_cases.json")
        if test_idx >= len(security_cases):
            pytest.skip(f"Test case {test_idx} not found")

        tc = security_cases[test_idx]
        print(f"\n{'='*60}")
        print(f"Testing Security Case: {tc['test_case_name']}")
        print(f"Description: {tc['description']}")
        print(f"{'='*60}")

        start = time.time()
        from app.core.security_agent import analyze_code_security

        result = await analyze_code_security(tc["code"], language=tc.get("language", "python"))
        duration_ms = (time.time() - start) * 1000

        print(f"\n✓ Response Time: {duration_ms:.0f}ms")

        # Basic structure
        assert isinstance(result, dict), "Result must be a dict"
        assert "vulnerabilities" in result and isinstance(result["vulnerabilities"], list)
        assert "security_score" in result

        # Check expected vulnerabilities are reported (if any)
        expected = [e.lower() for e in tc.get("expected_vulnerabilities", [])]
        found = [v.get("issue", "").lower() for v in result.get("vulnerabilities", [])]
        for exp in expected:
            assert any(exp in f for f in found), f"Expected vulnerability '{exp}' not found in {found}"

        # Check score bounds if provided
        if tc.get("expected_score_range"):
            rng = tc["expected_score_range"]
            sc = float(result.get("security_score", 0))
            assert rng["min"] <= sc <= rng["max"], f"Security score {sc} not in expected range {rng}"

        print(f"\n✅ Security Test '{tc['test_case_name']}' PASSED")


# Learning Flow Generator Tests
class TestLearningFlowGenerator:
            """Test suite for the Learning Flow generator."""

            @pytest.mark.asyncio
            @pytest.mark.parametrize("test_idx", range(len(load_test_cases(LEARNING_FIXTURES))))
            async def test_learning_flow(self, test_idx):
                """Verify generated learning flows match required structure and contents."""
                cases = load_test_cases(LEARNING_FIXTURES)
                if test_idx >= len(cases):
                    pytest.skip(f"Test case {test_idx} not found")

                tc = cases[test_idx]
                print(f"\n{'='*60}")
                print(f"Testing Learning Flow: {tc['test_case_name']}")
                print(f"Description: {tc['description']}")
                print(f"{'='*60}")

                import time
                start = time.time()

                from app.core.learning_agent import generate_learning_flow

                result = await generate_learning_flow(
                    topic=tc["topic"],
                    experience_level=tc["experience_level"],
                    weekly_hours=tc["weekly_hours"]
                )

                duration_ms = (time.time() - start) * 1000
                print(f"\n✓ Response Time: {duration_ms:.0f}ms (threshold: {tc.get('max_duration_ms', RESPONSE_TIME_THRESHOLD_MS)}ms)")

                # Basic structure checks
                assert isinstance(result, dict), "Result must be a dict-like JSON"
                assert "phases" in result and isinstance(result["phases"], list), "Missing phases array"
                phases = result["phases"]
                assert tc["expected_phases_min"] <= len(phases) <= tc["expected_phases_max"], f"Expected phases between {tc['expected_phases_min']}-{tc['expected_phases_max']}, got {len(phases)}"

                # Each phase should have at least 5 keyTopics
                for p in phases:
                    assert "keyTopics" in p and isinstance(p["keyTopics"], list), "Phase must include keyTopics list"
                    assert len(p["keyTopics"]) >= 5, "Each phase must include at least 5 keyTopics"

                # Projects and youtubeChannels checks
                assert "projects" in result and isinstance(result["projects"], list), "Missing projects array"
                assert len(result["projects"]) >= tc["expected_projects_min"], f"Expected at least {tc['expected_projects_min']} projects"
                assert "youtubeChannels" in result and isinstance(result["youtubeChannels"], list), "Missing youtubeChannels"
                assert len(result["youtubeChannels"]) >= tc["expected_youtube_min"], f"Expected at least {tc['expected_youtube_min']} YouTube channels"

                # Mermaid diagram must use graph TD and include newlines
                assert "mermaidDiagram" in result and "graph TD" in result["mermaidDiagram"], "Missing or invalid mermaidDiagram"
                assert "\n" in result["mermaidDiagram"], "mermaidDiagram must contain newlines"

                # Timeline should mention weeks and weekly hours
                assert "timeline" in result and str(tc["weekly_hours"]) in result["timeline"], "Timeline should include weekly hours"

                print(f"\n✅ Learning Flow '{tc['test_case_name']}' PASSED")
        
        # Authenticity Agent Tests
class TestAuthenticityAgent:
    """Test suite for Experience Authenticity agent."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_idx", range(6))  # 6 comprehensive test cases
    async def test_authenticity_analysis(self, test_idx, record_property):
        """Test authenticity analysis against expected outputs."""
        auth_test_cases = load_test_cases(AUTHENTICITY_FIXTURES)
        
        if test_idx >= len(auth_test_cases):
            pytest.skip(f"Test case {test_idx} not found")
        
        test_case = auth_test_cases[test_idx]
        test_name = test_case["test_case_name"]
        
        # Record test info
        record_property("test_case_name", test_name)
        record_property("description", test_case["description"])
        
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"Description: {test_case['description']}")
        print(f"{'='*60}")
        
        # Measure response time
        start_time = time.time()
        
        # Build input from test case
        resume = ResumeData(**test_case["resume_data"])
        
        github = None
        if test_case.get("github_evidence"):
            github = GitHubEvidence(**test_case["github_evidence"])
        
        leetcode = None
        if test_case.get("leetcode_evidence"):
            leetcode = LeetCodeEvidence(**test_case["leetcode_evidence"])
        
        auth_input = AuthenticityExtendedInput(
            resume=resume,
            github=github,
            leetcode=leetcode
        )
        
        # Run authenticity analysis
        result = await analyze_authenticity(auth_input)
        
        duration_ms = (time.time() - start_time) * 1000
        record_property("duration_ms", duration_ms)
        
        # Collect metrics
        metrics = {}
        
        # 1. Test authenticity score accuracy
        expected_range = test_case["expected_authenticity_score"]
        score_metric = score_accuracy(
            result.authenticity_score,
            expected_range["min"],
            expected_range["max"]
        )
        metrics["score_accuracy"] = score_metric
        record_property("score_accuracy", score_metric['accuracy'])
        record_property("actual_score", result.authenticity_score)
        record_property("expected_min", expected_range["min"])
        record_property("expected_max", expected_range["max"])
        print(f"\n✓ Authenticity Score: {result.authenticity_score} (expected {expected_range['min']}-{expected_range['max']})")
        print(f"  Accuracy: {score_metric['accuracy']:.2%}")
        
        # 2. Test confidence level match
        expected_confidence = test_case.get("expected_confidence_level", "")
        actual_confidence = result.confidence_level
        confidence_match = 1.0 if expected_confidence.lower() in actual_confidence.lower() else 0.0
        record_property("confidence_match", confidence_match)
        print(f"\n✓ Confidence Level: {actual_confidence} (expected: {expected_confidence})")
        
        # 3. Test risk indicators
        if test_case.get("expected_risk_flags"):
            risk_metric = substring_match(
                result.risk_indicators,
                test_case["expected_risk_flags"]
            )
            metrics["risk_flags"] = risk_metric
            record_property("risk_flags_match", risk_metric['match_rate'])
            print(f"\n✓ Risk Indicators Match: {risk_metric['match_rate']:.2%}")
            if risk_metric["missing"]:
                print(f"  Missing: {risk_metric['missing']}")
        
        # 4. Test strong evidence
        if test_case.get("expected_strengths"):
            strengths_metric = substring_match(
                result.strong_evidence,
                test_case["expected_strengths"]
            )
            metrics["strengths"] = strengths_metric
            record_property("strengths_match", strengths_metric['match_rate'])
            print(f"\n✓ Strong Evidence Match: {strengths_metric['match_rate']:.2%}")
        
        # 5. Test improvement suggestions (gaps)
        if test_case.get("expected_gaps"):
            gaps_metric = substring_match(
                result.improvement_suggestions,
                test_case["expected_gaps"]
            )
            metrics["gaps"] = gaps_metric
            record_property("gaps_match", gaps_metric['match_rate'])
            print(f"\n✓ Improvement Suggestions Match: {gaps_metric['match_rate']:.2%}")
        
        # 6. Test response time
        time_metric = response_time_check(duration_ms, RESPONSE_TIME_THRESHOLD_MS)
        metrics["response_time"] = time_metric
        record_property("response_time_ok", time_metric['passed'])
        print(f"\n✓ Response Time: {duration_ms:.0f}ms (threshold: {RESPONSE_TIME_THRESHOLD_MS}ms)")
        
        # Overall test pass criteria
        assert score_metric["passed"], f"Score {result.authenticity_score} not in expected range {expected_range}"
        
        print(f"\n✅ Test '{test_name}' PASSED")


# 
# Integration Tests
class TestIntegration:
    """Integration tests for the evaluation framework."""
    
    @pytest.mark.asyncio
    async def test_ats_with_no_job_description(self):
        """Test ATS analysis works without job description."""
        result = await analyze_ats(
            resume_text="Software Engineer with 5 years of Python experience.",
            job_description=None
        )
        
        assert result.ats_score >= 0
        assert result.ats_score <= 100
        assert isinstance(result.strengths, list)
        assert isinstance(result.issues, list)
    
    @pytest.mark.asyncio
    async def test_ats_empty_resume(self):
        """Test ATS handles empty resume gracefully."""
        result = await analyze_ats(
            resume_text="",
            job_description="Software Engineer position"
        )
        
        # Should still return valid structure even for empty input
        assert result.ats_score is not None
        assert isinstance(result.rejection_reasons, list)
    
    def test_eval_metrics_accuracy(self):
        """Test evaluation metrics calculations."""
        # Test score accuracy
        metric = score_accuracy(75, 70, 80)
        assert metric["passed"] == True
        assert metric["error"] == 0
        
        metric = score_accuracy(85, 70, 80)
        assert metric["passed"] == False
        assert metric["error"] == 5
    
    def test_keyword_overlap(self):
        """Test keyword overlap metric."""
        predicted = ["python", "java", "react"]
        expected = ["python", "javascript", "react"]
        
        metric = keyword_overlap(predicted, expected)
        assert 0 <= metric["jaccard_score"] <= 1
        assert "python" in metric["matched"]
        assert "react" in metric["matched"]


# Conftest fixture to save results
@pytest.fixture(scope="session", autouse=True)
def save_test_results(request):
    """Save test results after all tests complete."""
    yield
    # Results will be saved by the report generator


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
