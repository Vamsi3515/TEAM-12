# Evaluation Notes (Metrics, Tests, Guardrails, Limitations)

This document describes how the project’s AI agents are evaluated (what we measure, how to reproduce results), the guardrails in place, and current limitations.

---

## 0) Latest Evaluation Snapshot (from eval reports)

Below is the **latest measured snapshot** from the generated evaluation artifacts under `FastApi/eval_results/`.

### A) Agent-level pass rate / accuracy

| Agent | Tests | Passed | Pass rate | “Accuracy” fields available | Notes / Source report |
|------:|------:|------:|----------:|-----------------------------|------------------------|
| ATS | 16 | 16 | 100% | `average_score_accuracy = 1.0` + match-rate averages | `FastApi/eval_results/eval_ats_2025-12-14T04-50-00-043031.json` |
| Security Auditor | 15 | 15 | 100% | score-range checks enforced per fixture; aggregate `average_score_accuracy` not populated in this report | `FastApi/eval_results/eval_security_2025-12-14T05-51-19-982127.json` |
| Learning Flow | 3 | 3 | 100% | structure checks (phases/projects/youtube/mermaid/timeline); aggregate `average_score_accuracy` not populated in this report | `FastApi/eval_results/eval_learning_2025-12-14T05-09-08-084732.json` |
| Authenticity | 6 | 6 | 100% | structure/tone/guardrail tests (accuracy is pass/fail) | `FastApi/eval_results/pytest_report_authenticity_20251214_043939.json` |
| GitHub Analyzer | 0 | 0 | N/A | N/A | Latest `eval_github_*.json` reports show “No tests were run.” (often due to API/rate-limit constraints). |

### B) Quality & performance highlights (latest)

**ATS (latest)**
- Pass rate: **100%** (16/16)
- Score-in-range accuracy: **100%** (`average_score_accuracy = 1.0`)
- Average match rates (from report `metric_averages`):
  - strengths: **0.4669**
  - rejection_reasons: **0.1389**
  - issues: **0.1310**
  - suggestions: **0.0800**
- Performance: avg **5747 ms**, median **7621 ms**, max **10055 ms**
- Reports: `FastApi/eval_results/eval_ats_2025-12-14T04-50-00-043031.json` and `.html`

**Security Auditor (latest)**
- Pass rate: **100%** (15/15)
- Performance: avg **6435 ms**, median **9847 ms**, max **12088 ms**
- Report: `FastApi/eval_results/eval_security_2025-12-14T05-51-19-982127.json` and `.html`

**Learning Flow (latest)**
- Pass rate: **100%** (3/3)
- Performance: avg **19094 ms**, median **19152 ms**, max **19653 ms**
- Report: `FastApi/eval_results/eval_learning_2025-12-14T05-09-08-084732.json` and `.html`

**Authenticity (latest pytest report)**
- Pass rate: **100%** (6/6)
- Report: `FastApi/eval_results/pytest_report_authenticity_20251214_043939.json`

**GitHub Analyzer (status)**
- Latest `FastApi/eval_results/eval_github_2025-12-14T04-56-46-555574.json` indicates **no tests executed**.
- To generate a measurable GitHub pass rate, run:
  - `pytest tests/test_evals.py::TestGitHubAgent -v -s`
  - ensure `GITHUB_TOKEN` / `GITHUB_PAT` is set to avoid rate-limit skips.

---

## 1) Metrics (What we measure)

### 1.1) Which metrics apply to which agent (how we score)

This project centralizes reusable evaluation functions in `FastApi/app/core/eval_metrics.py`. The pytest suite then applies those functions per agent in `FastApi/tests/test_evals.py`.

**ATS Agent**
- `score_accuracy(...)`: verifies `ats_score` falls within each fixture’s `expected_score_range`.
- `substring_match(...)`: computes match rates for expected text inside:
  - `rejection_reasons`, `strengths`, `issues`, `suggestions`
- `response_time_check(...)`: ensures each test completes within the configured threshold.

**Security Auditor Agent**
- Fixture-driven correctness checks (in the pytest suite):
  - expected vulnerability keys must appear in the returned vulnerability list
  - `security_score` must fall within each fixture’s `expected_score_range`
- `response_time_check(...)`: ensures analysis completes within the configured threshold.

**GitHub Analyzer Agent**
- When GitHub tests are executed, the eval suite measures:
  - expected tech stack/keywords presence (string/list matching)
  - metric range checks for numeric metric outputs (where fixtures specify ranges)
  - `response_time_check(...)`
- Note: GitHub evals can be skipped/blocked by API rate limits if `GITHUB_TOKEN` / `GITHUB_PAT` is not provided.

**Authenticity Agent**
- Structure + policy guardrails are tested as correctness:
  - required JSON fields present (schema/structure validity)
  - tone constraints (no accusatory language) and supportive phrasing checks
- Timing is measured (response-time threshold check).

**Learning Flow Generator**
- Structure validity checks (pass/fail):
  - `phases` count within expected bounds
  - each phase has enough `keyTopics`
  - required sections present (`projects`, `youtubeChannels`, `mermaidDiagram`, etc.)
- `response_time_check(...)`.

### A) Functional correctness (fixture-based)
- **Score-in-range accuracy**: numeric outputs must fall within the `expected_*_range` bounds defined in fixtures.
- **Expected findings present**: required items (e.g., vulnerability keys) must appear in the output.

### B) Content quality (string overlap / match-rate)
- **Keyword/substring match rate (%)** for expected phrases in lists such as:
  - ATS: rejection reasons, strengths, issues, suggestions
  - GitHub: tech stack + qualitative observations
  - Authenticity: strong evidence, risk indicators, improvement suggestions

### C) Performance / reliability
- **Response time**: tests time each run and enforce a max threshold (default used by the eval suite is 30 seconds).
- **Robustness to malformed LLM output**: JSON parse/repair strategies + safe fallbacks (agent-dependent).

### D) Security Auditor-specific evaluation
- **Detection coverage**: 15 curated security cases spanning OWASP-style categories.
- **False-positive control**:
  - Static detection for high-signal patterns
  - AI findings are accepted only when corroborated by code heuristics (reduces hallucinated extras)
- **Security score (0–100)**: severity-weighted scoring designed to match expected score bands in fixtures.

---

## 2) Tests (How to reproduce)

### A) Install dependencies
```bash
cd FastApi
pip install -r requirements.txt
```

### B) Run all evaluation tests
```bash
cd FastApi
pytest tests/test_evals.py -v -s
```

### C) Run per-agent suites
```bash
cd FastApi
pytest tests/test_evals.py::TestATSAgent -v -s
pytest tests/test_evals.py::TestSecurityAgent -v -s
pytest tests/test_evals.py::TestLearningFlowGenerator -v -s
```

### D) Run eval runner (produces JSON + HTML reports)
```bash
cd FastApi
python -m app.eval_runner --agent ats
python -m app.eval_runner --agent github
python -m app.eval_runner --all
```

### E) Ground-truth fixtures
- ATS fixtures: `FastApi/tests/fixtures/ats_test_cases.json`
- GitHub fixtures: `FastApi/tests/fixtures/github_test_cases.json`
- Security fixtures: `FastApi/tests/fixtures/security_test_cases.json`

### F) Output artifacts
- Reports are written to: `FastApi/eval_results/` (both `.json` and `.html`)
- Baselines (if used): `FastApi/eval_results/baselines/`

---

## 3) Guardrails (Safety, consistency, and robustness)

### A) Output format guardrails
- Agents are prompted to output **strict JSON**.
- Outputs are validated (Pydantic schemas where implemented).
- JSON parse failures trigger:
  - repair attempt, then
  - safe fallback response (prevents API crashes).

### B) Authenticity Agent tone/ethics guardrails
- Designed as **decision support**, not a “fraud detector”.
- Enforced supportive wording (avoid accusatory language).
- Test coverage includes checks for forbidden/accusatory terms.

### C) Security Auditor guardrails
- Hybrid analysis pipeline: **static rules + RAG context + LLM**.
- False-positive reduction by corroboration checks before accepting AI-only findings.
- Bounded behavior:
  - prompt truncation to prevent token overflow
  - score bounded to `[0, 100]`

### D) Operational guardrails
- Error handling for external/API constraints (e.g., rate limits).
- Low-temperature LLM settings where possible for more stable eval results.

---

## 4) Limitations (Known constraints)

### A) LLM variability and external services
- Hosted LLM providers can change behavior over time.
- Network latency, provider load, and rate limits can affect runtime.

### B) Heuristic/static analysis limits
- Regex/heuristic detection can miss advanced cases (false negatives) or flag edge cases (false positives).
- Security agent is educational/assistive, not a replacement for professional SAST/DAST.

### C) RAG scope
- RAG quality depends on the curated knowledge entries; expanding/curating improves explanations and remediation guidance.

### D) Coverage tradeoffs
- GitHub analysis is naturally constrained by API availability, private repos, and rate limits.

### E) Evaluation scope
- Fixture-based evals validate representative scenarios; they do not guarantee perfect real-world performance across all frameworks/languages.
