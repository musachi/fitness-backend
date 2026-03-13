#!/usr/bin/env python3
"""
Test classification types to check if Position and Contraction Type exist
"""

import requests

def test_classification_types():
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
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test classification types
        types_response = requests.get(
            "http://127.0.0.1:8000/api/v1/classification-types",
            headers=headers
        )
        
        print(f"Classification Types Status: {types_response.status_code}")
        if types_response.status_code == 200:
            types = types_response.json()
            print("Available Classification Types:")
            for type_obj in types:
                print(f"  - {type_obj['name']} (ID: {type_obj['id']})")
        else:
            print(f"Error: {types_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_classification_types()
