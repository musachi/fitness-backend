#!/usr/bin/env python3
"""
Test exercises endpoint
"""

import requests

def test_exercises_endpoint():
    """Test exercises endpoint"""
    try:
        # First login
        login_data = {
            "username": "admin@fitness.com",
            "password": "admin123"
        }
        
        login_response = requests.post(
            "http://127.0.0.1:8000/api/v1/auth/login",
            data=login_data
        )
        
        if login_response.status_code != 200:
            print("❌ Login failed")
            return
        
        token = login_response.json()["access_token"]
        print(f"✅ Login successful!")
        
        # Test exercises endpoint
        headers = {"Authorization": f"Bearer {token}"}
        
        exercises_response = requests.get(
            "http://127.0.0.1:8000/api/v1/exercises/",
            headers=headers
        )
        
        print(f"\nExercises Status: {exercises_response.status_code}")
        print(f"Exercises Response: {exercises_response.text}")
        
        if exercises_response.status_code == 200:
            print("✅ Exercises endpoint working!")
        else:
            print("❌ Exercises endpoint failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_exercises_endpoint()
