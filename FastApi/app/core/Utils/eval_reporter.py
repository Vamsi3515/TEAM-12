"""Evaluation report generator for AI agents.

Generates comprehensive HTML and JSON reports from evaluation results,
including metrics, visualizations, and trend tracking.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import statistics


class EvalReporter:
    """Generate evaluation reports in various formats."""
    
    def __init__(self, results_dir: Optional[Path] = None):
        """Initialize reporter with results directory.
        
        Args:
            results_dir: Directory to store evaluation results
        """
        if results_dir is None:
            results_dir = Path(__file__).parent.parent.parent / "eval_results"
        
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(
        self,
        test_results: Dict[str, Any],
        agent_name: str,
        save: bool = True
    ) -> Dict[str, Any]:
        """Generate comprehensive evaluation report.
        
        Args:
            test_results: Dictionary of test results with metrics
            agent_name: Name of the agent being evaluated
            save: Whether to save report to disk
            
        Returns:
            Report dictionary
        """
        timestamp = datetime.now().isoformat()
        
        # Calculate aggregate statistics
        stats = self._calculate_statistics(test_results)
        
        # Build report
        report = {
            "agent": agent_name,
            "timestamp": timestamp,
            "summary": self._generate_summary(stats),
            "statistics": stats,
            "test_cases": self._format_test_cases(test_results),
            "failures": self._extract_failures(test_results),
            "performance": self._calculate_performance(test_results)
        }
        
        if save:
            # Save JSON report
            json_path = self._save_json_report(report, agent_name, timestamp)
            report["report_path"] = str(json_path)
            
            # Generate and save HTML report
            html_path = self._save_html_report(report, agent_name, timestamp)
            report["html_report_path"] = str(html_path)
        
        return report
    
    def _calculate_statistics(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate aggregate statistics from test results."""
        test_cases = test_results.get("test_cases", [])
        
        if not test_cases:
            return {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "pass_rate": 0.0
            }
        
        # Count outcomes
        total = len(test_cases)
        passed = sum(1 for tc in test_cases if tc.get("outcome") == "passed")
        failed = sum(1 for tc in test_cases if tc.get("outcome") == "failed")
        skipped = sum(1 for tc in test_cases if tc.get("outcome") == "skipped")
        
        # Calculate metric averages
        all_scores = []
        metric_averages = {}
        
        for tc in test_cases:
            if "_metrics" not in tc:
                continue
            
            metrics = tc["_metrics"]
            
            # Collect score accuracies
            if "score_accuracy" in metrics:
                all_scores.append(metrics["score_accuracy"].get("accuracy", 0))
            
            # Collect match rates
            for metric_name, metric_data in metrics.items():
                if isinstance(metric_data, dict) and "match_rate" in metric_data:
                    if metric_name not in metric_averages:
                        metric_averages[metric_name] = []
                    metric_averages[metric_name].append(metric_data["match_rate"])
        
        # Calculate averages
        avg_score_accuracy = statistics.mean(all_scores) if all_scores else 0.0
        
        for key in metric_averages:
            metric_averages[key] = statistics.mean(metric_averages[key])
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": passed / total if total > 0 else 0.0,
            "average_score_accuracy": avg_score_accuracy,
            "metric_averages": metric_averages
        }
    
    def _generate_summary(self, stats: Dict[str, Any]) -> str:
        """Generate human-readable summary."""
        total = stats["total_tests"]
        passed = stats["passed"]
        failed = stats["failed"]
        pass_rate = stats["pass_rate"]
        
        if total == 0:
            return "No tests were run."
        
        summary = f"Ran {total} test(s): {passed} passed, {failed} failed. "
        summary += f"Pass rate: {pass_rate:.1%}. "
        
        if pass_rate >= 0.9:
            summary += "✅ Excellent performance!"
        elif pass_rate >= 0.7:
            summary += "⚠️ Good performance with some issues."
        else:
            summary += "❌ Poor performance - requires attention."
        
        return summary
    
    def _format_test_cases(self, test_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format test case results for report."""
        test_cases = test_results.get("test_cases", [])
        formatted = []
        
        for tc in test_cases:
            formatted_tc = {
                "name": tc.get("test_case_name", "unknown"),
                "description": tc.get("description", ""),
                "outcome": tc.get("outcome", "unknown"),
                "duration_ms": tc.get("_duration_ms", 0)
            }
            
            # Add key metrics
            if "_metrics" in tc:
                metrics = tc["_metrics"]
                formatted_tc["metrics"] = {}
                
                if "score_accuracy" in metrics:
                    formatted_tc["metrics"]["score_accuracy"] = metrics["score_accuracy"]["accuracy"]
                
                for key in ["rejection_reasons", "strengths", "issues", "suggestions", "tech_stack"]:
                    if key in metrics and "match_rate" in metrics[key]:
                        formatted_tc["metrics"][key] = metrics[key]["match_rate"]
            
            formatted.append(formatted_tc)
        
        return formatted
    
    def _extract_failures(self, test_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract detailed information about failed tests."""
        test_cases = test_results.get("test_cases", [])
        failures = []
        
        for tc in test_cases:
            if tc.get("outcome") != "failed":
                continue
            
            failure = {
                "name": tc.get("test_case_name", "unknown"),
                "description": tc.get("description", ""),
                "error": tc.get("error", "Unknown error"),
                "expected": {},
                "actual": {}
            }
            
            # Extract expected vs actual for key fields
            if "_result" in tc:
                failure["actual"]["score"] = tc["_result"].get("ats_score")
            
            if "expected_score_range" in tc:
                failure["expected"]["score_range"] = tc["expected_score_range"]
            
            failures.append(failure)
        
        return failures
    
    def _calculate_performance(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance statistics."""
        test_cases = test_results.get("test_cases", [])
        durations = [tc.get("_duration_ms", 0) for tc in test_cases if "_duration_ms" in tc]
        
        if not durations:
            return {
                "avg_duration_ms": 0,
                "min_duration_ms": 0,
                "max_duration_ms": 0,
                "total_duration_ms": 0
            }
        
        return {
            "avg_duration_ms": statistics.mean(durations),
            "min_duration_ms": min(durations),
            "max_duration_ms": max(durations),
            "total_duration_ms": sum(durations),
            "median_duration_ms": statistics.median(durations)
        }
    
    def _save_json_report(self, report: Dict[str, Any], agent_name: str, timestamp: str) -> Path:
        """Save report as JSON file."""
        # Create filename with timestamp
        clean_timestamp = timestamp.replace(":", "-").replace(".", "-")
        filename = f"eval_{agent_name}_{clean_timestamp}.json"
        filepath = self.results_dir / filename
        
        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def _save_html_report(self, report: Dict[str, Any], agent_name: str, timestamp: str) -> Path:
        """Generate and save HTML report."""
        html_content = self._generate_html(report)
        
        # Create filename
        clean_timestamp = timestamp.replace(":", "-").replace(".", "-")
        filename = f"eval_{agent_name}_{clean_timestamp}.html"
        filepath = self.results_dir / filename
        
        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_html(self, report: Dict[str, Any]) -> str:
        """Generate HTML report."""
        stats = report["statistics"]
        summary = report["summary"]
        test_cases = report["test_cases"]
        failures = report["failures"]
        performance = report["performance"]
        
        # Determine status color
        pass_rate = stats["pass_rate"]
        if pass_rate >= 0.9:
            status_color = "#4CAF50"
            status_icon = "✅"
        elif pass_rate >= 0.7:
            status_color = "#FF9800"
            status_icon = "⚠️"
        else:
            status_color = "#F44336"
            status_icon = "❌"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluation Report - {report['agent']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            background: {status_color};
            color: white;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 15px;
        }}
        .content {{ padding: 30px; }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #fafafa;
            border-radius: 8px;
        }}
        .section h2 {{
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #333;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        .test-case {{
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid #ddd;
        }}
        .test-case.passed {{ border-left-color: #4CAF50; }}
        .test-case.failed {{ border-left-color: #F44336; }}
        .test-case.skipped {{ border-left-color: #FF9800; }}
        .test-case h3 {{ font-size: 1.1em; margin-bottom: 5px; }}
        .test-case p {{ color: #666; font-size: 0.9em; }}
        .metrics {{
            display: flex;
            gap: 15px;
            margin-top: 10px;
            flex-wrap: wrap;
        }}
        .metric {{
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .failure {{
            background: #ffebee;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid #F44336;
        }}
        .failure h3 {{ color: #c62828; margin-bottom: 8px; }}
        .failure .error {{ 
            background: white;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{status_icon} Evaluation Report</h1>
            <p><strong>Agent:</strong> {report['agent']}</p>
            <p><strong>Timestamp:</strong> {report['timestamp']}</p>
            <div class="status-badge">
                Pass Rate: {stats['pass_rate']:.1%}
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Summary</h2>
                <p>{summary}</p>
            </div>
            
            <div class="section">
                <h2>📈 Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Tests</h3>
                        <div class="value">{stats['total_tests']}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Passed</h3>
                        <div class="value" style="color: #4CAF50;">{stats['passed']}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Failed</h3>
                        <div class="value" style="color: #F44336;">{stats['failed']}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Avg Score Accuracy</h3>
                        <div class="value">{stats.get('average_score_accuracy', 0):.1%}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Avg Duration</h3>
                        <div class="value">{performance['avg_duration_ms']:.0f}ms</div>
                    </div>
                </div>
            </div>
"""
        
        # Add test cases
        if test_cases:
            html += """
            <div class="section">
                <h2>🧪 Test Cases</h2>
"""
            for tc in test_cases:
                outcome = tc.get("outcome", "unknown")
                name = tc.get("name", "Unknown")
                description = tc.get("description", "")
                duration = tc.get("duration_ms", 0)
                
                html += f"""
                <div class="test-case {outcome}">
                    <h3>{name}</h3>
                    <p>{description}</p>
                    <p><strong>Duration:</strong> {duration:.0f}ms</p>
"""
                
                if "metrics" in tc:
                    html += '<div class="metrics">'
                    for metric_name, metric_value in tc["metrics"].items():
                        if isinstance(metric_value, float):
                            html += f'<div class="metric"><strong>{metric_name}:</strong> {metric_value:.1%}</div>'
                    html += '</div>'
                
                html += """
                </div>
"""
            html += """
            </div>
"""
        
        # Add failures section
        if failures:
            html += """
            <div class="section">
                <h2>❌ Failures</h2>
"""
            for failure in failures:
                html += f"""
                <div class="failure">
                    <h3>{failure['name']}</h3>
                    <p>{failure['description']}</p>
                    <div class="error">{failure.get('error', 'Unknown error')}</div>
                </div>
"""
            html += """
            </div>
"""
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def compare_with_baseline(
        self,
        current_report: Dict[str, Any],
        baseline_path: Path
    ) -> Dict[str, Any]:
        """Compare current results with baseline.
        
        Args:
            current_report: Current evaluation report
            baseline_path: Path to baseline report JSON
            
        Returns:
            Comparison results
        """
        with open(baseline_path, 'r') as f:
            baseline = json.load(f)
        
        current_stats = current_report["statistics"]
        baseline_stats = baseline["statistics"]
        
        comparison = {
            "pass_rate_change": current_stats["pass_rate"] - baseline_stats["pass_rate"],
            "accuracy_change": (
                current_stats.get("average_score_accuracy", 0) - 
                baseline_stats.get("average_score_accuracy", 0)
            ),
            "regression": current_stats["pass_rate"] < baseline_stats["pass_rate"] * 0.95,
            "improvement": current_stats["pass_rate"] > baseline_stats["pass_rate"] * 1.05
        }
        
        return comparison


def generate_eval_report(
    test_results: Dict[str, Any],
    agent_name: str,
    save: bool = True
) -> Dict[str, Any]:
    """Convenience function to generate evaluation report.
    
    Args:
        test_results: Test results dictionary
        agent_name: Name of agent
        save: Whether to save report
        
    Returns:
        Generated report
    """
    reporter = EvalReporter()
    return reporter.generate_report(test_results, agent_name, save)
