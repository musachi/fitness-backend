#!/usr/bin/env python3
"""
Test classification values endpoint
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import httpx

async def test_classification_values():
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
            
            # Test classification types endpoint
            types_response = await client.get(
                "/api/v1/classification-types",
                headers=headers
            )
            
            print(f"Classification types status: {types_response.status_code}")
            if types_response.status_code == 200:
                types = types_response.json()
                print(f"Types: {len(types)}")
                
                # Test values for each type
                for type_obj in types[:3]:  # Test first 3 types
                    type_id = type_obj.get('id')
                    type_name = type_obj.get('name')
                    
                    values_response = await client.get(
                        f"/api/v1/classification-values?classification_type_id={type_id}",
                        headers=headers
                    )
                    
                    print(f"\n{type_name} (ID: {type_id}):")
                    print(f"  Status: {values_response.status_code}")
                    
                    if values_response.status_code == 200:
                        values = values_response.json()
                        print(f"  Values count: {len(values)}")
                        if values:
                            print(f"  First value: {values[0]}")
                    else:
                        print(f"  Error: {values_response.text}")
            else:
                print(f"Types error: {types_response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_classification_values())
