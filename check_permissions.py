import requests

def check_user_permissions():
    try:
        # Login
        login_data = {'username': 'admin@fitness.com', 'password': 'admin123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code != 200:
            print('❌ Login failed')
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get current user info
        user_response = requests.get('http://127.0.0.1:8000/api/v1/users/me', headers=headers)
        user_data = user_response.json()
        
        print("🔍 Current user info:")
        print(f"  ID: {user_data.get('id')}")
        print(f"  Email: {user_data.get('email')}")
        print(f"  Role: {user_data.get('role')}")
        print(f"  Is coach: {user_data.get('is_coach')}")
        print(f"  Is admin: {user_data.get('is_admin')}")
        print(f"  Coach approved: {user_data.get('coach_approved')}")
        
        # Try to get all users to see if admin has permissions
        users_response = requests.get('http://127.0.0.1:8000/api/v1/users', headers=headers)
        print(f"\n🔍 Can access users endpoint: {users_response.status_code}")
        
        # Check if there are any existing exercises
        exercises_response = requests.get('http://127.0.0.1:8000/api/v1/exercises', headers=headers)
        exercises_data = exercises_response.json()
        print(f"📊 Exercises in DB: {exercises_data.get('total', 0)}")
        
        # Try to create a simple exercise to see the exact error
        simple_exercise = {
            "name": "Test Exercise",
            "short_name": "Test",
            "description": "Test description",
            "unit": "Reps",
            "movement_type_id": 5,
            "muscle_group_id": 22,
            "equipment_id": 48,
            "goal_id": 1,
            "position_id": 59,
            "is_active": True
        }
        
        create_response = requests.post('http://127.0.0.1:8000/api/v1/exercises', json=simple_exercise, headers=headers)
        print(f"\n🔍 Create exercise response: {create_response.status_code}")
        print(f"🔍 Create exercise error: {create_response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_user_permissions()
