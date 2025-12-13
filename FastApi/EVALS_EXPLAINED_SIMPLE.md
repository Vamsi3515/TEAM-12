# What are Evals? A Simple Explanation

## 🎯 What are Evaluations (Evals)?

**Evals** are automated tests that check how well your AI agent is performing. Think of them like a report card for your AI.

### Simple Analogy
Imagine you're a teacher grading students:
- You give them a test (test case)
- They answer questions (AI generates output)
- You check if answers are correct (compare with expected results)
- You give them a score (metrics)

That's exactly what evals do for AI!

## 📝 How Our ATS Agent Evals Work

### 1. **Test Cases** (The Questions)
We have 16 different resume + job description scenarios:
- ✅ Perfect match candidate (should score 85-100)
- ❌ Junior applying for senior role (should score 15-35)
- ⚠️ Career changer (should score 45-65)
- And 13 more scenarios...

### 2. **Run the Agent** (Get the Answer)
For each test case:
- Feed the resume text to the ATS agent
- Agent analyzes it and returns:
  - ATS Score (0-100)
  - Rejection reasons
  - Strengths
  - Issues
  - Suggestions

### 3. **Compare with Expected Results** (Grading)
We check if the agent's output matches what we expect:

```
Test: Junior Developer applying for Senior Role

Expected:
- Score: 15-35 (low)
- Should mention: "lack of experience", "missing Python skills"
- Should suggest: "gain more experience"

Agent Output:
- Score: 82 ❌ FAIL (too high!)
- Mentions: "good React skills" ✅
- Missing: "years of experience needed" ❌

Result: FAILED - Agent scored too high for unqualified candidate
