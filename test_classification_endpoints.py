#!/usr/bin/env python3
"""
Test classification endpoints directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import httpx

async def test_endpoints():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        try:
            # Test without auth first
            print("=== Testing without authentication ===")
            
            # Test classification types
            types_response = await client.get("/api/v1/classification-types")
            print(f"Types status: {types_response.status_code}")
            if types_response.status_code == 200:
                types = types_response.json()
                print(f"Types count: {len(types)}")
                print(f"Types: {types}")
            else:
                print(f"Types error: {types_response.text}")
            
            # Test classification values for first type
            if types_response.status_code == 200:
                types = types_response.json()
                if types:
                    first_type_id = types[0]['id']
                    values_response = await client.get(f"/api/v1/classification-values?classification_type_id={first_type_id}")
                    print(f"Values status: {values_response.status_code}")
                    if values_response.status_code == 200:
                        values = values_response.json()
                        print(f"Values count: {len(values)}")
                        print(f"Values: {values}")
                    else:
                        print(f"Values error: {values_response.text}")
            
            print("\n=== Testing with authentication ===")
            
            # Login
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@fitness.com", "password": "admin123"}
            )
            
            if login_response.status_code != 200:
                print(f"Login failed: {login_response.status_code}")
                return
            
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test with auth
            types_auth_response = await client.get("/api/v1/classification-types", headers=headers)
            print(f"Types with auth status: {types_auth_response.status_code}")
            if types_auth_response.status_code == 200:
                types_auth = types_auth_response.json()
                print(f"Types with auth count: {len(types_auth)}")
                
                # Test values with auth
                if types_auth:
                    first_type_id = types_auth[0]['id']
                    values_auth_response = await client.get(f"/api/v1/classification-values?classification_type_id={first_type_id}", headers=headers)
                    print(f"Values with auth status: {values_auth_response.status_code}")
                    if values_auth_response.status_code == 200:
                        values_auth = values_auth_response.json()
                        print(f"Values with auth count: {len(values_auth)}")
                        print(f"Values with auth: {values_auth}")
                    else:
                        print(f"Values with auth error: {values_auth_response.text}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
