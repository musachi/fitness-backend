#!/usr/bin/env python3
"""
Test original backend login
"""

import requests

def test_original_login():
    """Test login with original backend"""
    try:
        login_data = {
            "username": "admin@fitness.com",
            "password": "admin123"
        }
        
        print("Testing original backend login...")
        response = requests.post(
            "http://localhost:8002/api/v1/auth/login",
            data=login_data
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()
        else:
            print("❌ Login failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_original_login()
