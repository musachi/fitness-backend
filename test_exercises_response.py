#!/usr/bin/env python3
"""
Test exercises endpoint response
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import httpx

async def test_exercises_endpoint():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        try:
            # First login to get token
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@fitness.com", "password": "admin123"}
            )
            
            if login_response.status_code != 200:
                print(f"Login failed: {login_response.status_code}")
                print(login_response.text)
                return
            
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test exercises endpoint
            exercises_response = await client.get(
                "/api/v1/exercises/?page=1&size=100",
                headers=headers
            )
            
            print(f"Exercises endpoint status: {exercises_response.status_code}")
            print(f"Response headers: {dict(exercises_response.headers)}")
            
            if exercises_response.status_code == 200:
                data = exercises_response.json()
                print(f"Response type: {type(data)}")
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                if isinstance(data, dict) and 'exercises' in data:
                    exercises = data['exercises']
                    print(f"Exercises type: {type(exercises)}")
                    print(f"Exercises length: {len(exercises) if isinstance(exercises, list) else 'Not a list'}")
                    print(f"First exercise type: {type(exercises[0]) if exercises and isinstance(exercises, list) else 'N/A'}")
                else:
                    print(f"Unexpected response structure: {data}")
            else:
                print(f"Error response: {exercises_response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_exercises_endpoint())
