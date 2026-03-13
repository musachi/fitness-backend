import requests

def debug_user_issue():
    try:
        print("🔍 Debugging user issue...")
        
        # Login
        login_data = {'username': 'admin@fitness.com', 'password': 'admin123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code != 200:
            print('❌ Login failed')
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        print("✅ Login successful, token received")
        
        # Try different endpoints to understand the issue
        endpoints_to_try = [
            '/users/me',
            '/users',
            '/auth/me'
        ]
        
        for endpoint in endpoints_to_try:
            try:
                response = requests.get(f'http://127.0.0.1:8000/api/v1{endpoint}', headers=headers)
                print(f"🔍 {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"  Data type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"  Keys: {list(data.keys())}")
                    else:
                        print(f"  Content: {data}")
                else:
                    print(f"  Error: {response.text}")
            except Exception as e:
                print(f"  Exception: {e}")
        
        # Try to create an exercise with the exact error details
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
        print(f"\n🔍 Create exercise details:")
        print(f"  Status: {create_response.status_code}")
        print(f"  Headers sent: {headers}")
        print(f"  Data sent: {simple_exercise}")
        print(f"  Response: {create_response.text}")
        
        # Let's try to create a user with different credentials to test
        print(f"\n🔍 Creating a new test user...")
        new_user_data = {
            "name": "Test Admin",
            "email": "testadmin@fitness.com",
            "password": "test123",
            "first_name": "Test",
            "last_name": "Admin",
            "role": "admin",
            "is_admin": True,
            "is_coach": True
        }
        
        register_response = requests.post('http://127.0.0.1:8000/api/v1/auth/register', json=new_user_data)
        print(f"  Register new user: {register_response.status_code}")
        
        if register_response.status_code == 201:
            # Login with new user
            new_login = {'username': 'testadmin@fitness.com', 'password': 'test123'}
            new_login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=new_login)
            
            if new_login_response.status_code == 200:
                new_token = new_login_response.json()['access_token']
                new_headers = {'Authorization': f'Bearer {new_token}'}
                
                # Try to get user info
                new_user_info = requests.get('http://127.0.0.1:8000/api/v1/auth/me', headers=new_headers)
                print(f"  New user info: {new_user_info.status_code}")
                if new_user_info.status_code == 200:
                    user_data = new_user_info.json()
                    print(f"  New user data: {user_data}")
                    print(f"  Is admin: {user_data.get('role')}")
                    print(f"  Is coach: {user_data.get('coach')}")
                else:
                    print(f"  New user error: {new_user_info.text}")
                
                # Try to create exercise with new user
                new_create_response = requests.post('http://127.0.0.1:8000/api/v1/exercises', json=simple_exercise, headers=new_headers)
                print(f"  Create exercise with new user: {new_create_response.status_code}")
                if new_create_response.status_code == 201:
                    print("✅ SUCCESS! New user can create exercises")
                else:
                    print(f"  New user error: {new_create_response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_user_issue()
