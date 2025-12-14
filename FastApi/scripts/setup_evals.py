"""
Setup script for evaluation framework.
Run this after installing requirements to verify setup.
"""

import sys
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed."""
    required = [
        'pytest',
        'pytest_asyncio',
        'sklearn',
        'numpy',
        'pandas'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def create_directories():
    """Create necessary directories."""
    base_dir = Path(__file__).parent.parent
    dirs = [
        base_dir / "eval_results",
        base_dir / "eval_results" / "baselines"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")

def verify_fixtures():
    """Verify test fixtures exist."""
    base_dir = Path(__file__).parent.parent
    fixtures = [
        base_dir / "tests" / "fixtures" / "ats_test_cases.json",
        base_dir / "tests" / "fixtures" / "github_test_cases.json"
    ]
    
    for fixture in fixtures:
        if fixture.exists():
            print(f"✅ Found: {fixture.name}")
        else:
            print(f"❌ Missing: {fixture.name}")
            return False
    
    return True

def main():
    """Run setup checks."""
    print("🔧 Setting up Evaluation Framework")
    print("=" * 60)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return 1
    else:
        print("✅ All dependencies installed")
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Verify fixtures
    print("\n📝 Verifying test fixtures...")
    if not verify_fixtures():
        print("❌ Some fixtures are missing")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run: python -m app.eval_runner --agent ats")
    print("2. Open generated HTML report in eval_results/")
    print("3. Read README_EVALS.md for more information")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
