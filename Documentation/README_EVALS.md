# AI Agent Evaluation Framework

Comprehensive evaluation (evals) framework for testing and monitoring the quality of ATS and GitHub analysis agents.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Test Cases](#test-cases)
- [Running Evaluations](#running-evaluations)
- [Understanding Reports](#understanding-reports)
- [Continuous Integration](#continuous-integration)
- [Adding New Test Cases](#adding-new-test-cases)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This evaluation framework provides:

- **Automated Testing**: Comprehensive test suites for both ATS and GitHub agents
- **Quality Metrics**: Score accuracy, keyword matching, semantic similarity, and more
- **Performance Tracking**: Response time monitoring and optimization
- **Regression Detection**: Automated comparison with baselines
- **Rich Reporting**: HTML and JSON reports with visualizations
- **CI/CD Integration**: GitHub Actions workflow for continuous evaluation

### Key Features

✅ 15+ ATS test cases covering various scenarios  
✅ 15+ GitHub test cases for repository analysis  
✅ Multiple evaluation metrics (accuracy, precision, recall, F1)  
✅ Beautiful HTML reports with statistics  
✅ Command-line interface for easy execution  
✅ Baseline comparison and regression detection  
✅ Automated CI/CD integration  

## 🚀 Quick Start

### Installation

1. Install dependencies:
```bash
cd FastApi
pip install -r requirements.txt
```

2. Verify installation:
```bash
pytest --version
python -m app.eval_runner --help
```

### Run Your First Evaluation

```bash
# Run ATS agent evaluation
python -m app.eval_runner --agent ats

# Run GitHub agent evaluation
python -m app.eval_runner --agent github

# Run all evaluations
python -m app.eval_runner --all
```

### View Results

After running evaluations, check:
- JSON reports: `eval_results/eval_ats_*.json`
- HTML reports: `eval_results/eval_ats_*.html`

Open the HTML report in your browser for a visual summary.

## 🏗️ Architecture

### Directory Structure

```
FastApi/
├── app/
│   ├── core/
│   │   ├── eval_metrics.py       # Evaluation metrics functions
│   │   └── eval_reporter.py      # Report generation
│   └── eval_runner.py            # CLI runner script
├── tests/
│   ├── fixtures/
│   │   ├── ats_test_cases.json   # ATS test scenarios
│   │   └── github_test_cases.json # GitHub test scenarios
│   ├── test_evals.py             # Main test suite
│   └── test_continuous_eval.py   # CI/CD tests
├── eval_results/                 # Generated reports
│   └── baselines/                # Baseline reports
└── .github/
    └── workflows/
        └── eval.yml              # GitHub Actions workflow
```

### Components

1. **Test Fixtures**: JSON files containing test cases with expected outputs
2. **Evaluation Metrics**: Python functions to compare predictions with expectations
3. **Test Suite**: Pytest-based tests that run agents and collect metrics
4. **Report Generator**: Creates HTML and JSON reports from test results
5. **CLI Runner**: Command-line interface for running evaluations
6. **CI/CD Integration**: Automated evaluation on PRs and commits

## 📝 Test Cases

### ATS Test Cases

Located in `tests/fixtures/ats_test_cases.json`, includes:

- ✅ Excellent matches (senior engineers with perfect fit)
- ❌ Experience mismatches (junior for senior role)
- 🔄 Career changers with transferable skills
- 🎯 Skill mismatches (data scientist for backend role)
- 💼 Overqualified candidates
- 📄 Missing keywords but good experience
- 🎓 Strong education, weak experience
- 🔧 Specialists applying for full-stack roles
- 🏢 Freelancers with diverse projects
- 🎓 Bootcamp graduates (entry-level)
- 🌍 International candidates
- ⏸️ Employment gaps
- And more...

### GitHub Test Cases

Located in `tests/fixtures/github_test_cases.json`, includes:

- ⭐ Well-maintained open source projects
- 📦 Personal portfolio projects
- 🚀 Active development projects
- 💤 Abandoned projects
- 🎨 React component libraries
- 📊 Data science projects
- 🤖 Machine learning projects
- 🎮 Gaming engines
- ⛓️ Blockchain implementations
- And more...

Each test case contains:
- Input data (resume, job description, repo URL)
- Expected outputs (scores, reasons, tech stack)
- Acceptable ranges for numeric values
- Expected keywords/phrases

## 🔄 Running Evaluations

### Basic Commands

```bash
# Run specific agent
python -m app.eval_runner --agent ats
python -m app.eval_runner --agent github

# Run all agents
python -m app.eval_runner --all

# Verbose output
python -m app.eval_runner --agent ats --verbose
```

### Comparison with Baseline

```bash
# Compare with previous baseline
python -m app.eval_runner --agent ats --compare-with-baseline

# Specify baseline file
python -m app.eval_runner --agent ats --compare-with-baseline --baseline-path eval_results/eval_ats_2024-01-01.json
```

### List Results

```bash
# List all evaluation results
python -m app.eval_runner --list
```

### Direct Pytest Execution

```bash
# Run specific test class
pytest tests/test_evals.py::TestATSAgent -v

# Run specific test
pytest tests/test_evals.py::TestATSAgent::test_ats_analysis[0] -v

# Run with detailed output
pytest tests/test_evals.py -v -s
```

## 📊 Understanding Reports

### JSON Report Structure

```json
{
  "agent": "ATS",
  "timestamp": "2024-12-13T10:30:00",
  "summary": "Ran 16 tests: 14 passed, 2 failed...",
  "statistics": {
    "total_tests": 16,
    "passed": 14,
    "failed": 2,
    "pass_rate": 0.875,
    "average_score_accuracy": 0.89
  },
  "test_cases": [...],
  "failures": [...],
  "performance": {
    "avg_duration_ms": 3500,
    "total_duration_ms": 56000
  }
}
```

### HTML Report Features

- 📈 **Summary Dashboard**: Overall pass rate and key metrics
- 📊 **Statistics Cards**: Visual breakdown of results
- 🧪 **Test Case Details**: Individual test outcomes with metrics
- ❌ **Failure Analysis**: Detailed error information
- ⚡ **Performance Metrics**: Response time statistics

### Interpreting Metrics

**Pass Rate**: Percentage of tests that passed
- ✅ 90%+ : Excellent
- ⚠️ 70-90%: Good with some issues
- ❌ <70%: Needs attention

**Score Accuracy**: How well predicted scores match expected ranges
- Closer to 1.0 (100%) is better

**Match Rate**: Percentage of expected keywords found in output
- Used for strengths, issues, suggestions, etc.

## 🔄 Continuous Integration

### GitHub Actions Setup

The evaluation framework includes a GitHub Actions workflow (`.github/workflows/eval.yml`) that:

1. **On Pull Requests**: Runs evaluations and checks for regressions
2. **On Push to Main**: Runs full evaluation suite
3. **Nightly Schedule**: Daily evaluation runs
4. **Manual Trigger**: Run on-demand from GitHub UI

### Setting Up CI/CD

1. **Add Secrets** to your GitHub repository:
   - `GROQ_API_KEY`: Your Groq API key
   - `GITHUB_TOKEN`: Automatically provided by GitHub

2. **Create Baselines**:
```bash
# Run evaluations to establish baseline
python -m app.eval_runner --all

# Copy reports to baselines directory
mkdir -p eval_results/baselines
cp eval_results/eval_ats_*.json eval_results/baselines/baseline_ats.json
cp eval_results/eval_github_*.json eval_results/baselines/baseline_github.json
```

3. **Commit and Push**:
```bash
git add eval_results/baselines/
git commit -m "Add evaluation baselines"
git push
```

### Quality Thresholds

Configurable in `tests/test_continuous_eval.py`:

```python
MIN_PASS_RATE = 0.80        # 80% minimum
MIN_SCORE_ACCURACY = 0.70   # 70% minimum
```

PRs will fail if:
- Pass rate drops below threshold
- Major regression detected (>5% performance drop)
- Structural validation fails

## ➕ Adding New Test Cases

### Adding ATS Test Cases

Edit `tests/fixtures/ats_test_cases.json`:

```json
{
  "test_case_name": "descriptive_name",
  "description": "Brief description",
  "resume_text": "Full resume text...",
  "job_description": "Job description...",
  "expected_score_range": {
    "min": 70,
    "max": 85
  },
  "expected_rejection_reasons": ["keyword1", "keyword2"],
  "expected_strengths": ["strength1", "strength2"],
  "expected_issues": ["issue1"],
  "expected_suggestions": ["suggestion1"]
}
```

### Adding GitHub Test Cases

Edit `tests/fixtures/github_test_cases.json`:

```json
{
  "test_case_name": "descriptive_name",
  "description": "Brief description",
  "repo_url": "owner/repo or full URL",
  "expected_tech_stack": ["python", "django"],
  "expected_metrics_ranges": {
    "code_quality": {"min": 70, "max": 90},
    "documentation": {"min": 75, "max": 95}
  },
  "expected_strengths": ["well documented"],
  "expected_weaknesses": ["limited tests"],
  "expected_suggestions": ["add ci/cd"]
}
```

### Tips for Good Test Cases

1. **Be Specific**: Use concrete examples, not generic text
2. **Set Realistic Ranges**: Allow some flexibility in score ranges
3. **Use Keywords**: Include key terms you expect to see
4. **Cover Edge Cases**: Test boundary conditions
5. **Document Intent**: Clear descriptions help debugging

## ⚙️ Configuration

### Metric Thresholds

Edit `tests/test_evals.py`:

```python
RESPONSE_TIME_THRESHOLD_MS = 30000  # 30 seconds
```

### Evaluation Settings

Modify metrics behavior in `app/core/eval_metrics.py`:

```python
def keyword_overlap(..., case_sensitive=False):
    # Set case_sensitive=True for stricter matching
```

### Report Customization

Customize report styling in `app/core/eval_reporter.py`:

```python
# Change HTML template colors, layout, etc.
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Tests fail with API quota errors  
**Solution**: Check your API keys in `.env` file. Consider using mocks for CI.

**Issue**: All tests are skipped  
**Solution**: Ensure test fixtures exist and are valid JSON.

**Issue**: Report generation fails  
**Solution**: Check write permissions for `eval_results/` directory.

**Issue**: Import errors when running tests  
**Solution**: Run from FastApi directory: `cd FastApi && pytest tests/test_evals.py`

### Debug Mode

Run with verbose output:
```bash
python -m app.eval_runner --agent ats --verbose
pytest tests/test_evals.py -v -s
```

### Skipping Flaky Tests

```bash
# Skip GitHub tests (may hit rate limits)
pytest tests/test_evals.py -k "not TestGitHubAgent"
```

## 📈 Best Practices

### Regular Evaluation

1. **Before Major Changes**: Run evals to establish baseline
2. **After Changes**: Compare with baseline to catch regressions
3. **Weekly**: Review trends in evaluation results
4. **On PR**: Automated checks prevent quality degradation

### Maintaining Test Cases

1. **Review Failures**: Understand why tests fail
2. **Update Expectations**: Adjust ranges as agents improve
3. **Add Edge Cases**: Cover issues found in production
4. **Remove Outdated**: Clean up irrelevant test cases

### Performance Optimization

1. **Mock External APIs**: For faster CI runs
2. **Parallel Execution**: Use pytest-xdist for speed
3. **Cache Results**: Store intermediate results
4. **Selective Running**: Test only changed agents

## 🤝 Contributing

To contribute new test cases or metrics:

1. Add test cases to fixtures
2. Update this README with new scenarios
3. Run evaluations to verify
4. Submit PR with baseline comparison

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Evaluation Best Practices](https://github.com/openai/evals)

## 📧 Support

For issues or questions:
- Check troubleshooting section
- Review test output logs
- Check evaluation reports for details

---

**Happy Evaluating! 🚀**
