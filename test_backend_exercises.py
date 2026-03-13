import requests

def test_backend():
    try:
        # Test if backend is running
        response = requests.get('http://127.0.0.1:8000/api/v1/health')
        print('✅ Backend is running:', response.status_code)
        
        # Test exercises endpoint
        login_data = {'username': 'admin@fitness.com', 'password': 'admin123'}
        login_response = requests.post('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            
            exercises_response = requests.get('http://127.0.0.1:8000/api/v1/exercises', headers=headers)
            print('🔍 Exercises endpoint status:', exercises_response.status_code)
            print('🔍 Exercises response structure:', type(exercises_response.json()))
            
            response_json = exercises_response.json()
            if isinstance(response_json, dict):
                print('🔍 Exercises response keys:', list(response_json.keys()))
                if 'exercises' in response_json:
                    print('✅ Exercises key found, count:', len(response_json['exercises']))
                else:
                    print('❌ Exercises key NOT found in response')
            else:
                print('❌ Response is not a dict, it\'s:', type(response_json))
                print('🔍 Response content:', response_json)
        else:
            print('❌ Login failed:', login_response.status_code)
            print('🔍 Login error:', login_response.text)
            
    except Exception as e:
        print('❌ Backend not running or connection error:', e)

if __name__ == "__main__":
    test_backend()
