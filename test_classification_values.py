#!/usr/bin/env python3
"""
Test classification values endpoints
"""

import requests

def test_classification_values():
    try:
        # Login first
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
            print(f"Status: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("🔍 Testing classification values endpoints...")
        
        # Test each classification type
        classification_types = [
            {"name": "Movement Type", "id": 1},
            {"name": "Goal", "id": 4},
            {"name": "Muscle Group", "id": 6},
            {"name": "Equipment", "id": 7},
            {"name": "Position", "id": 8},
            {"name": "Units", "id": 9}
        ]
        
        for type_info in classification_types:
            print(f"\n📋 Testing {type_info['name']} (ID: {type_info['id']})")
            
            # Test the endpoint frontend is using
            values_response = requests.get(
                f"http://127.0.0.1:8000/api/v1/classification-values?classification_type_id={type_info['id']}",
                headers=headers
            )
            
            print(f"  Status: {values_response.status_code}")
            
            if values_response.status_code == 200:
                values = values_response.json()
                if isinstance(values, list):
                    print(f"  Values found: {len(values)}")
                    for value in values[:3]:  # Show first 3
                        print(f"    - ID: {value.get('id')}, Value: {value.get('value')}")
                else:
                    print(f"  Response type: {type(values)}")
                    print(f"  Response: {values}")
            else:
                print(f"  Error: {values_response.text}")
        
        # Also test specific endpoints that might exist
        print(f"\n🔍 Testing specific endpoints...")
        
        specific_endpoints = [
            "/api/v1/exercises/movement-types",
            "/api/v1/exercises/muscle-groups", 
            "/api/v1/exercises/equipment",
            "/api/v1/exercises/positions",
            "/api/v1/exercises/goals"
        ]
        
        for endpoint in specific_endpoints:
            print(f"\n📡 Testing {endpoint}")
            response = requests.get(
                f"http://127.0.0.1:8000{endpoint}",
                headers=headers
            )
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                if isinstance(data, dict) and 'movement_types' in data:
                    print(f"  Movement types: {len(data['movement_types'])}")
                elif isinstance(data, dict) and 'muscle_groups' in data:
                    print(f"  Muscle groups: {len(data['muscle_groups'])}")
                elif isinstance(data, dict) and 'equipment' in data:
                    print(f"  Equipment: {len(data['equipment'])}")
                elif isinstance(data, dict) and 'positions' in data:
                    print(f"  Positions: {len(data['positions'])}")
                elif isinstance(data, dict) and 'goals' in data:
                    print(f"  Goals: {len(data['goals'])}")
            else:
                print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_classification_values()
