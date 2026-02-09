import os
import sys
import uuid

import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"


def test_api_endpoints():
    """Test API endpoints using requests"""
    print("🚀 Testing API Endpoints with requests...")

    # 1. Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/health")
        if response.status_code == 200:
            print(f"✅ Health check: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("⚠️  Make sure the server is running: python -m src.main")
        return

    # 2. Test registration
    print("\n2. Testing user registration...")
    test_suffix = uuid.uuid4().hex[:8]
    register_data = {
        "name": "API Test User",
        "email": f"api_test_{test_suffix}@example.com",
        "password": "test123",
        "role_id": 3,  # Assuming 3 is client
    }

    try:
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/auth/register", json=register_data
        )
        if response.status_code == 201:
            print(f"✅ Registration successful: {response.json()['email']}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return

    # 3. Test login (using form data for OAuth2 compatibility)
    print("\n3. Testing login...")
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }

    try:
        # IMPORTANT: Use data= for form data (OAuth2 style)
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/auth/login",
            data=login_data,  # data= not json= for form data
        )
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("✅ Login successful, token received")
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return

    # 4. Test protected endpoint (me)
    print("\n4. Testing protected endpoint (me)...")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/auth/me", headers=headers)
        if response.status_code == 200:
            me_data = response.json()
            print(f"✅ Me endpoint: {me_data['email']}")
            print(f"   User ID: {me_data['id']}")
            print(f"   Name: {me_data['name']}")
        else:
            print(f"❌ Me endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Me endpoint error: {e}")

    # 5. Test exercises endpoint (public)
    print("\n5. Testing exercises endpoint...")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/exercises/")
        if response.status_code == 200:
            exercises = response.json()
            ex_count = len(exercises.get("exercises", []))
            print(f"✅ Exercises endpoint: {ex_count} exercises")
            print(f"   Total: {exercises.get('total', 0)}")
        else:
            print(f"❌ Exercises endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exercises endpoint error: {e}")

    # 6. Test categories endpoint
    print("\n6. Testing categories endpoint...")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/exercises/categories/")
        if response.status_code == 200:
            categories = response.json()
            cat_count = len(categories.get("categories", []))
            print(f"✅ Categories endpoint: {cat_count} categories")
        else:
            print(f"❌ Categories endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Categories endpoint error: {e}")

    # 7. Test users endpoint (should fail without admin access)
    print("\n7. Testing users endpoint (should require admin)...")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/users/", headers=headers)
        if response.status_code == 403:
            print("✅ Users endpoint correctly requires admin (403 Forbidden)")
        elif response.status_code == 200:
            print("⚠️  Users endpoint accessible (might be admin user)")
        else:
            print(f"❌ Users endpoint: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Users endpoint error: {e}")

    print("\n🎉 All API tests completed!")

    print("\n" + "=" * 50)
    print("📚 API Documentation available at:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc:      {BASE_URL}/redoc")
    print("=" * 50)


if __name__ == "__main__":
    # Run tests
    test_api_endpoints()
