"""Test Security API endpoint via HTTP request."""

import requests
import json


def test_security_api():
    """Test the security API endpoint."""
    
    base_url = "http://localhost:8000"
    
    # Test cases
    test_cases = [
        {
            "name": "SQL Injection",
            "payload": {
                "code": 'cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")',
                "language": "python",
                "file_name": "vulnerable.py"
            }
        },
        {
            "name": "Hardcoded Secret",
            "payload": {
                "code": 'API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz123456"',
                "language": "python"
            }
        },
        {
            "name": "Secure Code",
            "payload": {
                "code": '''from sqlalchemy import text
def get_user(user_id: int, db):
    query = text("SELECT * FROM users WHERE id = :user_id")
    return db.execute(query, {"user_id": user_id})''',
                "language": "python"
            }
        }
    ]
    
    print("=" * 70)
    print("🔒 Testing Security Auditor API")
    print("=" * 70)
    
    # Test health endpoint first
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/security/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running:")
        print("   cd FastApi && uvicorn app.main:app --reload")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test analysis endpoint
    print("\n2. Testing analysis endpoint...")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'─' * 70}")
        print(f"Test Case {i}: {test_case['name']}")
        print(f"{'─' * 70}")
        
        try:
            response = requests.post(
                f"{base_url}/api/security/analyze",
                json=test_case['payload'],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis successful")
                print(f"\n  Score: {result['security_score']}/100")
                print(f"  Risk: {result['overall_risk'].upper()}")
                print(f"  Vulnerabilities: {len(result['vulnerabilities'])}")
                
                if result['vulnerabilities']:
                    print(f"\n  Found Issues:")
                    for vuln in result['vulnerabilities'][:3]:
                        print(f"    • {vuln['title']} ({vuln['severity']})")
                else:
                    print(f"\n  ✅ No vulnerabilities detected!")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out (>30s)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'=' * 70}")
    print("✅ API Testing Complete")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    test_security_api()
