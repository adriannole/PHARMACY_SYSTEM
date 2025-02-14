import requests

BASE_URL = "http://localhost:4006"

def test_login_success():
    
    payload = {
        "username": "moran",
        "password": "123456"  
    }

    response = requests.post(f"{BASE_URL}/login", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Login successful"
    assert data.get("username") == "moran"  

def test_login_failure():
    
    payload = {
        "username": "moran",
        "password": "wrongpassword"  
    }

    response = requests.post(f"{BASE_URL}/login", json=payload)

    assert response.status_code == 401  
    data = response.json()
    assert data.get("error") == "Invalid username or password"
