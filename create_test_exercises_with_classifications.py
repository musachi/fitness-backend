#!/usr/bin/env python3
"""
Create test exercises with classifications
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import httpx

async def create_test_exercises():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        try:
            # Login to get token
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@fitness.com", "password": "admin123"}
            )
            
            if login_response.status_code != 200:
                print(f"Login failed: {login_response.status_code}")
                return
            
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get classification values
            types_response = await client.get("/api/v1/classification-types", headers=headers)
            types = types_response.json()
            
            # Get values for each type
            values_by_type = {}
            for type_obj in types:
                values_response = await client.get(
                    f"/api/v1/classification-values?classification_type_id={type_obj['id']}",
                    headers=headers
                )
                values_by_type[type_obj['name']] = values_response.json()
            
            print("Classification values loaded:")
            for type_name, values in values_by_type.items():
                print(f"  {type_name}: {len(values)} values")
            
            # Create test exercises
            test_exercises = [
                {
                    "name": "Sentadilla con barra",
                    "short_name": "Squat",
                    "description": "Ejercicio básico de piernas",
                    "movement_type_id": values_by_type.get("Movement Type", [{}])[0].get("id"),
                    "muscle_group_id": values_by_type.get("Muscle Group", [{}])[0].get("id"),
                    "equipment_id": values_by_type.get("Equipment", [{}])[0].get("id"),
                    "position_id": values_by_type.get("Position", [{}])[0].get("id"),
                    "is_active": True
                },
                {
                    "name": "Press de banca",
                    "short_name": "Bench Press",
                    "description": "Ejercicio básico de pecho",
                    "movement_type_id": values_by_type.get("Movement Type", [{}])[0].get("id"),
                    "muscle_group_id": values_by_type.get("Muscle Group", [{}])[1].get("id") if len(values_by_type.get("Muscle Group", [])) > 1 else values_by_type.get("Muscle Group", [{}])[0].get("id"),
                    "equipment_id": values_by_type.get("Equipment", [{}])[0].get("id"),
                    "position_id": values_by_type.get("Position", [{}])[1].get("id") if len(values_by_type.get("Position", [])) > 1 else values_by_type.get("Position", [{}])[0].get("id"),
                    "is_active": True
                },
                {
                    "name": "Flexión de brazos",
                    "short_name": "Push-up",
                    "description": "Ejercicio con peso corporal",
                    "movement_type_id": values_by_type.get("Movement Type", [{}])[1].get("id") if len(values_by_type.get("Movement Type", [])) > 1 else values_by_type.get("Movement Type", [{}])[0].get("id"),
                    "muscle_group_id": values_by_type.get("Muscle Group", [{}])[4].get("id") if len(values_by_type.get("Muscle Group", [])) > 4 else values_by_type.get("Muscle Group", [{}])[0].get("id"),
                    "equipment_id": values_by_type.get("Equipment", [{}])[2].get("id") if len(values_by_type.get("Equipment", [])) > 2 else values_by_type.get("Equipment", [{}])[0].get("id"),
                    "position_id": values_by_type.get("Position", [{}])[0].get("id"),
                    "is_active": True
                }
            ]
            
            print(f"\nCreating {len(test_exercises)} test exercises...")
            
            for i, exercise in enumerate(test_exercises):
                # Skip if any required field is missing
                if not all(exercise.values()):
                    print(f"Skipping exercise {i+1} - missing required fields")
                    continue
                
                response = await client.post("/api/v1/exercises/", json=exercise, headers=headers)
                
                if response.status_code == 200:
                    print(f"✅ Created: {exercise['name']}")
                else:
                    print(f"❌ Failed to create {exercise['name']}: {response.status_code}")
                    print(f"   Error: {response.text}")
            
            # Verify created exercises
            exercises_response = await client.get("/api/v1/exercises/?page=1&size=100", headers=headers)
            if exercises_response.status_code == 200:
                exercises = exercises_response.json()
                print(f"\n✅ Total exercises in database: {exercises['total']}")
                for exercise in exercises['exercises'][:3]:
                    print(f"  - {exercise['name']} ({exercise['short_name']})")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_exercises())
