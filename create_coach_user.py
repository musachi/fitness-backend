import requests

def create_coach_user():
    try:
        print("🔍 Creating coach user...")
        
        # Create coach user
        coach_data = {
            "name": "Coach User",
            "email": "coach@fitness.com",
            "password": "coach123",
            "first_name": "Coach",
            "last_name": "User",
            "role": "coach",
            "is_admin": False,
            "is_coach": True
        }
        
        # Register coach
        register_response = requests.post('http://127.0.0.1:8000/api/v1/auth/register', json=coach_data)
        print(f"🔍 Register coach response: {register_response.status_code}")
        
        if register_response.status_code == 201:
            print("✅ Coach user registered successfully")
        elif register_response.status_code == 400:
            print("ℹ️ Coach user already exists")
        else:
            print(f"❌ Register failed: {register_response.text}")
            return
        
        # Login as coach
        login_data = {'username': 'coach@fitness.com', 'password': 'coach123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code != 200:
            print('❌ Coach login failed')
            print(f'Login error: {login_response.text}')
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        print("✅ Coach login successful")
        
        # Get coach info
        coach_info = requests.get('http://127.0.0.1:8000/api/v1/auth/me', headers=headers)
        if coach_info.status_code == 200:
            coach_data = coach_info.json()
            print("✅ Coach info:")
            print(f"  ID: {coach_data.get('id')}")
            print(f"  Name: {coach_data.get('name')}")
            print(f"  Role ID: {coach_data.get('role_id')}")
            print(f"  Role: {coach_data.get('role')}")
        
        # Try to create exercise as coach
        simple_exercise = {
            "name": "Test Exercise by Coach",
            "short_name": "TestC",
            "description": "Test description by coach",
            "unit": "Reps",
            "movement_type_id": 5,
            "muscle_group_id": 22,
            "equipment_id": 48,
            "goal_id": 1,
            "position_id": 59,
            "is_active": True
        }
        
        create_response = requests.post('http://127.0.0.1:8000/api/v1/exercises', json=simple_exercise, headers=headers)
        print(f"\n🔍 Create exercise as coach: {create_response.status_code}")
        
        if create_response.status_code == 201:
            print("✅ SUCCESS! Coach can create exercises")
            
            # Verify it was created
            exercises_response = requests.get('http://127.0.0.1:8000/api/v1/exercises', headers=headers)
            exercises_data = exercises_response.json()
            print(f"📊 Total exercises now: {exercises_data.get('total', 0)}")
            
            # List the exercises
            if exercises_data.get('exercises'):
                print("📋 Exercises created:")
                for ex in exercises_data['exercises']:
                    print(f"  - {ex.get('name')} ({ex.get('short_name')})")
        else:
            print(f"❌ Create exercise failed: {create_response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_coach_user()
