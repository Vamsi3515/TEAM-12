"""Quick test script for Security Auditor Agent."""

import asyncio
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.Agents.security_agent import analyze_code_security


# Test cases
test_codes = {
    "sql_injection": """
def get_user(user_id):
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()
""",
    "hardcoded_secret": """
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz123456"
def authenticate():
    return API_KEY
""",
    "secure_code": """
from sqlalchemy import text

def get_user_secure(user_id: int, db):
    query = text("SELECT * FROM users WHERE id = :user_id")
    result = db.execute(query, {"user_id": user_id})
    return result.fetchone()
"""
}


async def test_security_agent():
    """Test the security agent with sample code."""
    
    print("=" * 70)
    print("🔒 SECURITY AUDITOR AGENT - Quick Test")
    print("=" * 70)
    
    for test_name, code in test_codes.items():
        print(f"\n\n{'='*70}")
        print(f"TEST: {test_name}")
        print(f"{'='*70}")
        print(f"Code:\n{code}")
        print(f"\n{'─'*70}")
        print("Analyzing...")
        print(f"{'─'*70}\n")
        
        try:
            result = await analyze_code_security(code=code, language="python")
            
            print(f"✅ ANALYSIS COMPLETE")
            print(f"\n📊 Results:")
            print(f"  • Security Score: {result.security_score}/100")
            print(f"  • Risk Level: {result.overall_risk.upper()}")
            print(f"  • Static Findings: {result.static_findings_count}")
            print(f"  • AI Enhanced: {result.ai_enhanced}")
            
            if result.vulnerabilities:
                print(f"\n🚨 Vulnerabilities Found ({len(result.vulnerabilities)}):")
                for i, vuln in enumerate(result.vulnerabilities, 1):
                    print(f"\n  {i}. {vuln.title}")
                    print(f"     Severity: {vuln.severity.upper()}")
                    print(f"     Category: {vuln.category}")
                    print(f"     CWE: {vuln.cwe_id}")
                    print(f"     Lines: {vuln.line_numbers}")
                    print(f"     Fix: {vuln.remediation}")
            else:
                print(f"\n✅ No vulnerabilities found!")
            
            if result.security_strengths:
                print(f"\n💪 Strengths:")
                for strength in result.security_strengths:
                    print(f"  • {strength}")
            
            if result.recommendations:
                print(f"\n💡 Recommendations:")
                for rec in result.recommendations[:3]:
                    print(f"  • {rec}")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n\n{'='*70}")
    print("✅ ALL TESTS COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(test_security_agent())
