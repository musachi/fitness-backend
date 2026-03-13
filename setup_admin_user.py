import requests

def setup_admin_user():
    try:
        print("🔍 Setting up admin user...")
        
        # First, try to register admin user
        admin_data = {
            "name": "Admin User",
            "email": "admin@fitness.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "User",
            "role": "admin",
            "is_admin": True,
            "is_coach": True
        }
        
        # Try to register
        register_response = requests.post('http://127.0.0.1:8000/api/v1/auth/register', json=admin_data)
        print(f"🔍 Register response: {register_response.status_code}")
        
        if register_response.status_code == 201:
            print("✅ Admin user registered successfully")
        elif register_response.status_code == 400:
            print("ℹ️ Admin user already exists, trying to update...")
        else:
            print(f"❌ Register failed: {register_response.text}")
            return
        
        # Now try to login
        login_data = {'username': 'admin@fitness.com', 'password': 'admin123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code != 200:
            print('❌ Login still failed')
            print(f'Login error: {login_response.text}')
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get user info after login
        user_response = requests.get('http://127.0.0.1:8000/api/v1/users/me', headers=headers)
        user_data = user_response.json()
        
        print("✅ User info after login:")
        print(f"  ID: {user_data.get('id')}")
        print(f"  Email: {user_data.get('email')}")
        print(f"  Role: {user_data.get('role')}")
        print(f"  Is admin: {user_data.get('is_admin')}")
        print(f"  Is coach: {user_data.get('is_coach')}")
        print(f"  Coach approved: {user_data.get('coach_approved')}")
        
        # If user exists but is not admin, try to update
        if user_data.get('id') and not user_data.get('is_admin'):
            print("🔧 Updating user to admin...")
            update_data = {
                "role": "admin",
                "is_admin": True,
                "is_coach": True
            }
            
            update_response = requests.put(f'http://127.0.0.1:8000/api/v1/users/{user_data["id"]}', json=update_data, headers=headers)
            print(f"🔍 Update response: {update_response.status_code}")
            
            if update_response.status_code == 200:
                print("✅ User updated to admin successfully")
            else:
                print(f"❌ Update failed: {update_response.text}")
        
        # Now try to create an exercise
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
        
        if create_response.status_code == 201:
            print("✅ Test exercise created successfully!")
            
            # Verify it was created
            exercises_response = requests.get('http://127.0.0.1:8000/api/v1/exercises', headers=headers)
            exercises_data = exercises_response.json()
            print(f"📊 Total exercises now: {exercises_data.get('total', 0)}")
        else:
            print(f"❌ Create exercise failed: {create_response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_admin_user()
