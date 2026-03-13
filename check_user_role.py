import requests

def check_user_role():
    try:
        print("🔍 Checking user role...")
        
        # Login
        login_data = {'username': 'admin@fitness.com', 'password': 'admin123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code != 200:
            print('❌ Login failed')
            return
        
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get user info
        user_info = requests.get('http://127.0.0.1:8000/api/v1/auth/me', headers=headers)
        if user_info.status_code == 200:
            user_data = user_info.json()
            print("✅ User info:")
            print(f"  ID: {user_data.get('id')}")
            print(f"  Name: {user_data.get('name')}")
            print(f"  Email: {user_data.get('email')}")
            print(f"  Role ID: {user_data.get('role_id')}")
            print(f"  Role: {user_data.get('role')}")
            print(f"  Coach info: {user_data.get('coach')}")
            
            # Check what role_id is expected
            role_id = user_data.get('role_id')
            if role_id == 1:
                print("⚠️ User is admin (role_id=1) but exercises endpoint requires coach (role_id=2)")
            elif role_id == 2:
                print("✅ User is coach (role_id=2) - should have access")
            else:
                print(f"❓ User has unknown role_id: {role_id}")
                
        else:
            print(f"❌ Failed to get user info: {user_info.text}")
        
        # Try to create exercise as admin (should fail)
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
        print(f"\n🔍 Create exercise as admin: {create_response.status_code}")
        print(f"  Error: {create_response.text}")
        
        # Now let's see if we can change the endpoint to accept admins too
        print(f"\n🔧 SOLUTION: Change exercises endpoint to accept both admins AND coaches")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_user_role()
