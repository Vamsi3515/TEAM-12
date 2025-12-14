"""Helper script to create evaluation baselines.

Run this after your first successful evaluation to establish baseline metrics.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


def find_latest_report(agent: str, results_dir: Path) -> Path:
    """Find the most recent evaluation report for an agent."""
    pattern = f"eval_{agent}_*.json"
    reports = list(results_dir.glob(pattern))
    
    if not reports:
        return None
    
    # Sort by modification time, most recent first
    reports.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return reports[0]


def create_baseline(agent: str):
    """Create baseline from latest evaluation report."""
    results_dir = Path(__file__).parent / "eval_results"
    baselines_dir = results_dir / "baselines"
    
    # Find latest report
    latest_report = find_latest_report(agent, results_dir)
    
    if not latest_report:
        print(f"❌ No evaluation report found for {agent} agent")
        print(f"   Run: python -m app.eval_runner --agent {agent}")
        return False
    
    # Create baselines directory if needed
    baselines_dir.mkdir(parents=True, exist_ok=True)
    
    # Create baseline
    baseline_path = baselines_dir / f"baseline_{agent}.json"
    
    # Backup existing baseline if it exists
    if baseline_path.exists():
        backup_path = baselines_dir / f"baseline_{agent}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        shutil.copy(baseline_path, backup_path)
        print(f"📦 Backed up existing baseline to: {backup_path.name}")
    
    # Copy latest report as baseline
    shutil.copy(latest_report, baseline_path)
    
    # Load and display stats
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    
    stats = baseline.get("statistics", {})
    
    print(f"✅ Created baseline for {agent.upper()} agent")
    print(f"   Source: {latest_report.name}")
    print(f"   Baseline: {baseline_path.name}")
    print(f"\n📊 Baseline Statistics:")
    print(f"   Total Tests: {stats.get('total_tests', 0)}")
    print(f"   Pass Rate: {stats.get('pass_rate', 0):.1%}")
    print(f"   Avg Accuracy: {stats.get('average_score_accuracy', 0):.1%}")
    
    return True


def main():
    """Main function to create baselines."""
    print("🎯 Baseline Creation Tool")
    print("=" * 60)
    
    results_dir = Path(__file__).parent / "eval_results"
    
    if not results_dir.exists():
        print("❌ No eval_results directory found")
        print("   Run evaluations first:")
        print("   python -m app.eval_runner --all")
        return 1
    
    # Create baselines for both agents
    agents = ["ats", "github"]
    success_count = 0
    
    for agent in agents:
        print(f"\n📝 Creating baseline for {agent.upper()} agent...")
        if create_baseline(agent):
            success_count += 1
        print()
    
    print("=" * 60)
    if success_count == len(agents):
        print(f"✅ Successfully created {success_count} baselines!")
        print("\nNext steps:")
        print("1. Commit baselines: git add eval_results/baselines/")
        print("2. Run comparison: python -m app.eval_runner --agent ats --compare-with-baseline")
    else:
        print(f"⚠️ Created {success_count}/{len(agents)} baselines")
        print("Run evaluations for missing agents")
    
    return 0 if success_count == len(agents) else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
