#!/usr/bin/env python3
"""
Test frontend login connection
"""

import requests

def test_frontend_login():
    """Test login from frontend perspective"""
    try:
        # Test the exact same request frontend would make
        login_data = {
            "username": "admin@fitness.com",
            "password": "admin123"
        }
        
        print("Testing frontend login connection...")
        print(f"URL: http://127.0.0.1:8002/api/v1/auth/login")
        print(f"Data: {login_data}")
        
        response = requests.post(
            "http://127.0.0.1:8002/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            print(f"Token: {token_data.get('access_token', 'N/A')[:20]}...")
            return True
        else:
            print("❌ Login failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_frontend_login()
