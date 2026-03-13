import requests

def create_test_exercises():
    try:
        # Login
        login_data = {'username': 'admin@fitness.com', 'password': 'admin123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code != 200:
            print('❌ Login failed')
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get classification values
        types_response = requests.get('http://127.0.0.1:8000/api/v1/classification-types', headers=headers)
        classification_types = types_response.json()
        
        print("📋 Creating test exercises...")
        
        # Create test exercises
        test_exercises = [
            {
                "name": "Cuclillas (Squats)",
                "short_name": "Cclls",
                "description": "Ejercicio fundamental para piernas",
                "unit": "Libras",
                "movement_type_id": 5,  # Leg Extension
                "muscle_group_id": 22,  # Legs-Posterior
                "equipment_id": 48,     # Barbell
                "goal_id": 1,           # Hypertrophy
                "position_id": 59,      # Static
                "is_active": True
            },
            {
                "name": "Press de Banca",
                "short_name": "Pss Bnc",
                "description": "Ejercicio para pecho",
                "unit": "Libras",
                "movement_type_id": 16,  # Compound LE + IAE
                "muscle_group_id": 23,   # Legs
                "equipment_id": 48,      # Barbell
                "goal_id": 2,            # Maximum Strength
                "position_id": 59,       # Static
                "is_active": True
            },
            {
                "name": "Sentadillas con Salto",
                "short_name": "Sntd Sl",
                "description": "Ejercicio explosivo para piernas",
                "unit": "Reps",
                "movement_type_id": 6,   # Hip Extension
                "muscle_group_id": 21,   # Legs-Anterior
                "equipment_id": 50,      # Kettlebell
                "goal_id": 71,           # Maximum-Strength Strength-Endurance Hypertrophy
                "position_id": 60,      # With movement
                "is_active": True
            }
        ]
        
        created_count = 0
        for exercise_data in test_exercises:
            try:
                response = requests.post('http://127.0.0.1:8000/api/v1/exercises', json=exercise_data, headers=headers)
                if response.status_code == 201:
                    print(f"✅ Created: {exercise_data['name']}")
                    created_count += 1
                else:
                    print(f"❌ Failed to create {exercise_data['name']}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"❌ Error creating {exercise_data['name']}: {e}")
        
        print(f"\n🎉 Created {created_count} test exercises successfully!")
        
        # Verify exercises were created
        verify_response = requests.get('http://127.0.0.1:8000/api/v1/exercises', headers=headers)
        exercises = verify_response.json()
        print(f"📊 Total exercises in database: {exercises.get('total', 0)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_test_exercises()
