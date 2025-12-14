"""
Quick integration test for the authenticity agent endpoint.
Run this to verify the API is working before testing from frontend.
"""

import requests
import json

def test_authenticity_endpoint():
    url = "http://localhost:8000/api/analyze-authenticity"
    
    # Sample request matching AuthenticityExtendedInput schema
    payload = {
        "resume": {
            "raw_text": "Software Engineer with 3 years of experience in Python and React. Built multiple web applications.",
            "skills": ["Python", "React", "JavaScript"],
            "projects": [
                {
                    "name": "react-dashboard",
                    "description": "A React-based dashboard application",
                    "technologies": ["React", "JavaScript"]
                }
            ],
            "certifications": ["AWS Solutions Architect"],
            "experience": [],
            "education": []
        },
        "evidences": [
            {
                "type": "github_repo",
                "url": "https://github.com/user/react-dashboard",
                "title": "react-dashboard",
                "metadata": {
                    "stars": 10,
                    "commits": 25,
                    "readme_quality": "good"
                }
            },
            {
                "type": "certificate",
                "url": "https://example.com/cert/aws",
                "title": "AWS Solutions Architect",
                "metadata": {
                    "issuer_verified": True
                }
            },
            {
                "type": "github_profile",
                "url": "https://github.com/user",
                "title": "user",
                "metadata": {}
            }
        ],
        "additional_context": "Test candidate profile"
    }
    
    print("Sending request to:", url)
    print("\nPayload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(url, json=payload)
        
        print("\n" + "="*50)
        print(f"Status Code: {response.status_code}")
        print("="*50)
        
        if response.ok:
            result = response.json()
            print("\n✅ SUCCESS! Response:")
            print(json.dumps(result, indent=2))
        else:
            print("\n❌ ERROR!")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        print("Make sure the FastAPI server is running: uvicorn app.main:app --reload")

if __name__ == "__main__":
    test_authenticity_endpoint()
