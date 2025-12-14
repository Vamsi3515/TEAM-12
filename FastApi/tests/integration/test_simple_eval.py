"""Simple smoke test for evaluation framework."""

import json
from pathlib import Path
from app.core.Utils.eval_metrics import (
        score_accuracy,
        keyword_overlap,
        substring_match,
        json_structure_validity,
        response_time_check,
        aggregate_metrics
    )
from app.core.Agents.ats_agent import analyze_ats
from app.core.Utils.eval_reporter import EvalReporter
from app.core.Agents.github_agent import analyze_github_repo


def test_ats_fixtures_exist():
    """Verify ATS test fixtures exist and are valid."""
    fixtures_path = Path(__file__).parent / "fixtures" / "ats_test_cases.json"
    assert fixtures_path.exists(), f"ATS fixtures not found at {fixtures_path}"
    
    with open(fixtures_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    
    assert len(test_cases) > 0, "ATS test cases are empty"
    assert isinstance(test_cases, list), "ATS test cases should be a list"
    
    # Verify structure of first test case
    first_case = test_cases[0]
    required_fields = ["test_case_name", "description", "resume_text", "expected_score_range"]
    for field in required_fields:
        assert field in first_case, f"Missing required field: {field}"
    
    print(f"✅ Found {len(test_cases)} ATS test cases")


def test_github_fixtures_exist():
    """Verify GitHub test fixtures exist and are valid."""
    fixtures_path = Path(__file__).parent / "fixtures" / "github_test_cases.json"
    assert fixtures_path.exists(), f"GitHub fixtures not found at {fixtures_path}"
    
    with open(fixtures_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    
    assert len(test_cases) > 0, "GitHub test cases are empty"
    assert isinstance(test_cases, list), "GitHub test cases should be a list"
    
    # Verify structure of first test case
    first_case = test_cases[0]
    required_fields = ["test_case_name", "description", "repo_url"]
    for field in required_fields:
        assert field in first_case, f"Missing required field: {field}"
    
    print(f"✅ Found {len(test_cases)} GitHub test cases")


def test_eval_metrics_importable():
    """Verify evaluation metrics module can be imported."""
    
    
    # Test a simple metric calculation
    result = score_accuracy(75, 70, 80)
    assert "passed" in result
    assert "accuracy" in result
    assert result["passed"] is True
    
    print("✅ All evaluation metrics imported successfully")


def test_ats_agent_importable():
    """Verify ATS agent can be imported."""
    
    print("✅ ATS agent imported successfully")


def test_github_agent_importable():
    """Verify GitHub agent can be imported."""
    
    print("✅ GitHub agent imported successfully")


def test_eval_reporter_importable():
    """Verify evaluation reporter can be imported."""
    
    reporter = EvalReporter()
    assert reporter.results_dir.exists()
    
    print("✅ Evaluation reporter created successfully")
