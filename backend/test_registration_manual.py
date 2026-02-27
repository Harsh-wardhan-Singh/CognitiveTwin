"""
Test script to diagnose registration errors
Run from backend directory: python -m pytest tests/test_registration.py -v -s
Or run manually: python test_registration_manual.py
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

def test_registration():
    """Test registration endpoint and display detailed errors"""
    
    test_cases = [
        {
            "name": "Valid registration",
            "data": {
                "email": "testuser@example.com",
                "password": "password123",
                "role": "student"
            }
        },
        {
            "name": "Invalid email format",
            "data": {
                "email": "invalidemail",
                "password": "password123",
                "role": "student"
            }
        },
        {
            "name": "Missing role",
            "data": {
                "email": "test@example.com",
                "password": "password123"
            }
        },
        {
            "name": "Invalid role",
            "data": {
                "email": "test@example.com",
                "password": "password123",
                "role": "admin"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test_case['name']}")
        print(f"Payload: {json.dumps(test_case['data'], indent=2)}")
        print('='*60)
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/register",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {json.dumps(response.json(), indent=2)}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Testing Registration Endpoint")
    print(f"API Base URL: {API_BASE_URL}")
    test_registration()
