# Evaluation Framework - Quick Reference

## 🚀 Common Commands

### Run Evaluations
```bash
# ATS agent only
python -m app.eval_runner --agent ats

# GitHub agent only
python -m app.eval_runner --agent github

# Both agents
python -m app.eval_runner --all

# With verbose output
python -m app.eval_runner --agent ats --verbose
```

### Baseline Management
```bash
# Create baselines from latest results
python create_baselines.py

# Compare with baseline
python -m app.eval_runner --agent ats --compare-with-baseline

# Specify baseline file
python -m app.eval_runner --agent ats --compare-with-baseline --baseline-path eval_results/baselines/baseline_ats.json
```

### View Results
```bash
# List all evaluation results
python -m app.eval_runner --list

# Open HTML report (after running eval)
# Windows: start eval_results/eval_ats_*.html
# Mac: open eval_results/eval_ats_*.html
# Linux: xdg-open eval_results/eval_ats_*.html
```

### Direct Pytest
```bash
# Run all evals
pytest tests/test_evals.py -v

# Run only ATS tests
pytest tests/test_evals.py::TestATSAgent -v

# Run specific test
pytest tests/test_evals.py::TestATSAgent::test_ats_analysis[0] -v

# Run with output
pytest tests/test_evals.py -v -s
```

## 📁 Important Files

### Test Data
- `tests/fixtures/ats_test_cases.json` - ATS test scenarios
- `tests/fixtures/github_test_cases.json` - GitHub test scenarios

### Core Modules
- `app/core/eval_metrics.py` - Metric calculations
- `app/core/eval_reporter.py` - Report generation
- `app/eval_runner.py` - CLI interface

### Test Suites
- `tests/test_evals.py` - Main evaluation tests
- `tests/test_continuous_eval.py` - CI/CD quality checks

### Results
- `eval_results/*.json` - JSON reports
- `eval_results/*.html` - HTML reports
- `eval_results/baselines/` - Baseline reports

### Documentation
- `README_EVALS.md` - Full documentation
- `EVAL_IMPLEMENTATION_SUMMARY.md` - Implementation details

## 📊 Understanding Metrics

### Pass Rate
- **90%+** ✅ Excellent
- **70-90%** ⚠️ Good with issues
- **<70%** ❌ Needs attention

### Score Accuracy
- Checks if predicted score is within expected range
- 1.0 (100%) = perfect accuracy

### Match Rate
- Percentage of expected keywords found
- Used for strengths, issues, suggestions

### Response Time
- Current threshold: 30 seconds
- Tracks performance over time

## 🔧 Quick Fixes

### Problem: Tests failing
**Solution**: Check API keys in `.env` file
```bash
GROQ_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
```

### Problem: Import errors
**Solution**: Run from FastApi directory
```bash
cd FastApi
python -m app.eval_runner --agent ats
```

### Problem: No baselines found
**Solution**: Create baselines first
```bash
python -m app.eval_runner --all
python create_baselines.py
```

### Problem: Slow tests
**Solution**: Skip GitHub tests (may hit API limits)
```bash
pytest tests/test_evals.py -k "not TestGitHubAgent"
```

## ➕ Adding Test Cases

### ATS Test Case Template
```json
{
  "test_case_name": "unique_name",
  "description": "What this tests",
  "resume_text": "...",
  "job_description": "...",
  "expected_score_range": {"min": 70, "max": 85},
  "expected_rejection_reasons": ["keyword1"],
  "expected_strengths": ["keyword2"],
  "expected_issues": ["keyword3"],
  "expected_suggestions": ["keyword4"]
}
```

### GitHub Test Case Template
```json
{
  "test_case_name": "unique_name",
  "description": "What this tests",
  "repo_url": "owner/repo",
  "expected_tech_stack": ["python", "django"],
  "expected_metrics_ranges": {
    "code_quality": {"min": 70, "max": 90}
  },
  "expected_strengths": ["keyword1"],
  "expected_weaknesses": ["keyword2"],
  "expected_suggestions": ["keyword3"]
}
```

## 🎯 Workflow Examples

### Development Workflow
```bash
# 1. Before changes
python -m app.eval_runner --agent ats
python create_baselines.py

# 2. Make your changes...

# 3. After changes
python -m app.eval_runner --agent ats --compare-with-baseline

# 4. Review report
# Open eval_results/eval_ats_*.html
```

### CI/CD Workflow
```bash
# Automatic on PR:
# - Runs evaluations
# - Compares with baseline
# - Comments on PR
# - Fails if regression detected

# Manual trigger from GitHub UI:
# Actions → AI Agent Evaluations → Run workflow
```

### Monitoring Workflow
```bash
# Weekly check
python -m app.eval_runner --all
python -m app.eval_runner --list

# Review trends in reports
# Update baselines if needed
```

## ⚙️ Configuration

### Modify Thresholds
Edit `tests/test_continuous_eval.py`:
```python
MIN_PASS_RATE = 0.80        # 80%
MIN_SCORE_ACCURACY = 0.70   # 70%
```

### Modify Response Time Limit
Edit `tests/test_evals.py`:
```python
RESPONSE_TIME_THRESHOLD_MS = 30000  # 30 seconds
```

### Modify Report Style
Edit `app/core/eval_reporter.py`:
```python
# Change HTML colors, layout, etc.
```

## 📞 Get Help

1. Read [README_EVALS.md](README_EVALS.md) - Full documentation
2. Check troubleshooting section
3. Review test output with `--verbose`
4. Examine HTML reports for details

## 🎓 Best Practices

✅ Run evals before major changes  
✅ Create baselines after first run  
✅ Review failures carefully  
✅ Update test cases as needed  
✅ Monitor trends over time  
✅ Use CI/CD integration  
✅ Keep baselines in version control  

---

**Quick Start**: `python -m app.eval_runner --agent ats`
