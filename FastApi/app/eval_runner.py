"""CLI runner for AI agent evaluations.

Run evaluations from command line with various options:
- python -m app.eval_runner --agent ats
- python -m app.eval_runner --agent github --save-results
- python -m app.eval_runner --all --compare-with-baseline
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.core.eval_reporter import EvalReporter


class EvalRunner:
    """Evaluation runner with CLI interface."""
    
    def __init__(self, verbose: bool = False):
        """Initialize runner.
        
        Args:
            verbose: Whether to print verbose output
        """
        self.verbose = verbose
        self.results_dir = Path(__file__).parent.parent / "eval_results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.reporter = EvalReporter(self.results_dir)
    
    def run_ats_evals(self, save_results: bool = True) -> dict:
        """Run ATS agent evaluations.
        
        Args:
            save_results: Whether to save results to disk
            
        Returns:
            Evaluation results dictionary
        """
        print("🚀 Running ATS Agent Evaluations...")
        print("=" * 60)
        
        # Run pytest for ATS tests
        test_file = Path(__file__).parent.parent / "tests" / "test_evals.py"
        
        # Prepare pytest arguments
        pytest_args = [
            str(test_file),
            "-v",
            "-k", "TestATSAgent",
            "--tb=short",
            "-p", "no:warnings"
        ]
        
        if self.verbose:
            pytest_args.append("-s")
        
        # Run tests and capture results
        result = pytest.main(pytest_args)
        
        # Parse results
        eval_results = {
            "agent": "ATS",
            "timestamp": datetime.now().isoformat(),
            "test_cases": [],
            "exit_code": result
        }
        
        # Generate report if save_results is True
        if save_results:
            print("\n📊 Generating evaluation report...")
            report = self.reporter.generate_report(eval_results, "ats", save=True)
            print(f"✅ Report saved to: {report.get('report_path')}")
            print(f"📄 HTML report: {report.get('html_report_path')}")
            return report
        
        return eval_results
    
    def run_github_evals(self, save_results: bool = True) -> dict:
        """Run GitHub agent evaluations.
        
        Args:
            save_results: Whether to save results to disk
            
        Returns:
            Evaluation results dictionary
        """
        print("🚀 Running GitHub Agent Evaluations...")
        print("=" * 60)
        
        # Run pytest for GitHub tests
        test_file = Path(__file__).parent.parent / "tests" / "test_evals.py"
        
        pytest_args = [
            str(test_file),
            "-v",
            "-k", "TestGitHubAgent",
            "--tb=short",
            "-p", "no:warnings"
        ]
        
        if self.verbose:
            pytest_args.append("-s")
        
        result = pytest.main(pytest_args)
        
        eval_results = {
            "agent": "GitHub",
            "timestamp": datetime.now().isoformat(),
            "test_cases": [],
            "exit_code": result
        }
        
        if save_results:
            print("\n📊 Generating evaluation report...")
            report = self.reporter.generate_report(eval_results, "github", save=True)
            print(f"✅ Report saved to: {report.get('report_path')}")
            print(f"📄 HTML report: {report.get('html_report_path')}")
            return report
        
        return eval_results
    
    def run_all_evals(self, save_results: bool = True) -> dict:
        """Run all agent evaluations.
        
        Args:
            save_results: Whether to save results
            
        Returns:
            Combined results dictionary
        """
        print("🚀 Running All Agent Evaluations...")
        print("=" * 60)
        
        ats_results = self.run_ats_evals(save_results)
        print("\n" + "=" * 60 + "\n")
        github_results = self.run_github_evals(save_results)
        
        combined = {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "ats": ats_results,
                "github": github_results
            }
        }
        
        return combined
    
    def compare_with_baseline(
        self,
        agent: str,
        baseline_path: Optional[Path] = None
    ) -> dict:
        """Compare current results with baseline.
        
        Args:
            agent: Agent name (ats or github)
            baseline_path: Path to baseline report (auto-detected if None)
            
        Returns:
            Comparison results
        """
        print(f"📊 Comparing {agent.upper()} agent with baseline...")
        
        # Run current evaluation
        if agent == "ats":
            current_report = self.run_ats_evals(save_results=True)
        elif agent == "github":
            current_report = self.run_github_evals(save_results=True)
        else:
            raise ValueError(f"Unknown agent: {agent}")
        
        # Find baseline if not provided
        if baseline_path is None:
            baseline_path = self._find_latest_baseline(agent)
        
        if baseline_path is None or not baseline_path.exists():
            print("⚠️ No baseline found. This will be the baseline.")
            return {"status": "no_baseline", "current": current_report}
        
        # Compare
        print(f"📈 Comparing with baseline: {baseline_path}")
        comparison = self.reporter.compare_with_baseline(current_report, baseline_path)
        
        # Print comparison results
        print("\n" + "=" * 60)
        print("COMPARISON RESULTS")
        print("=" * 60)
        print(f"Pass Rate Change: {comparison['pass_rate_change']:+.1%}")
        print(f"Accuracy Change: {comparison['accuracy_change']:+.1%}")
        
        if comparison['regression']:
            print("❌ REGRESSION DETECTED - Performance decreased significantly")
            return {"status": "regression", "comparison": comparison, "exit_code": 1}
        elif comparison['improvement']:
            print("✅ IMPROVEMENT - Performance increased significantly")
            return {"status": "improvement", "comparison": comparison, "exit_code": 0}
        else:
            print("➡️ STABLE - Performance within acceptable range")
            return {"status": "stable", "comparison": comparison, "exit_code": 0}
    
    def _find_latest_baseline(self, agent: str) -> Optional[Path]:
        """Find most recent baseline report for agent."""
        pattern = f"eval_{agent}_*.json"
        reports = list(self.results_dir.glob(pattern))
        
        if not reports:
            return None
        
        # Sort by modification time
        reports.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Return second most recent (first is current run)
        return reports[1] if len(reports) > 1 else reports[0]
    
    def list_results(self):
        """List all evaluation results."""
        print("📊 Evaluation Results")
        print("=" * 60)
        
        json_reports = list(self.results_dir.glob("eval_*.json"))
        html_reports = list(self.results_dir.glob("eval_*.html"))
        
        if not json_reports:
            print("No evaluation results found.")
            return
        
        print(f"\nFound {len(json_reports)} evaluation reports:\n")
        
        for report_path in sorted(json_reports, key=lambda p: p.stat().st_mtime, reverse=True):
            stat = report_path.stat()
            timestamp = datetime.fromtimestamp(stat.st_mtime)
            
            # Load report to get summary
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            agent = report.get("agent", "unknown")
            pass_rate = report.get("statistics", {}).get("pass_rate", 0)
            
            print(f"📄 {report_path.name}")
            print(f"   Agent: {agent}")
            print(f"   Pass Rate: {pass_rate:.1%}")
            print(f"   Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run AI agent evaluations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m app.eval_runner --agent ats
  python -m app.eval_runner --agent github --save-results
  python -m app.eval_runner --all
  python -m app.eval_runner --agent ats --compare-with-baseline
  python -m app.eval_runner --list
        """
    )
    
    parser.add_argument(
        "--agent",
        choices=["ats", "github"],
        help="Which agent to evaluate"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run evaluations for all agents"
    )
    
    parser.add_argument(
        "--save-results",
        action="store_true",
        default=True,
        help="Save evaluation results to disk (default: True)"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to disk"
    )
    
    parser.add_argument(
        "--compare-with-baseline",
        action="store_true",
        help="Compare results with baseline and check for regression"
    )
    
    parser.add_argument(
        "--baseline-path",
        type=Path,
        help="Path to specific baseline report for comparison"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all evaluation results"
    )
    
    args = parser.parse_args()
    
    # Create runner
    runner = EvalRunner(verbose=args.verbose)
    
    # Handle list command
    if args.list:
        runner.list_results()
        return 0
    
    # Determine save_results flag
    save_results = args.save_results and not args.no_save
    
    try:
        # Run evaluations
        if args.compare_with_baseline:
            if not args.agent:
                print("❌ Error: --compare-with-baseline requires --agent")
                return 1
            
            result = runner.compare_with_baseline(args.agent, args.baseline_path)
            return result.get("exit_code", 0)
        
        elif args.all:
            runner.run_all_evals(save_results)
            return 0
        
        elif args.agent == "ats":
            runner.run_ats_evals(save_results)
            return 0
        
        elif args.agent == "github":
            runner.run_github_evals(save_results)
            return 0
        
        else:
            parser.print_help()
            return 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Evaluation interrupted by user")
        return 130
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
