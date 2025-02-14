import requests
import random

BASE_URL = "http://localhost:4007"

def generate_unique_username(base_username):

    random_number = random.randint(100000, 999999)
    return f"{base_username}_{random_number}"

def test_register_success():
    
    username = generate_unique_username("test_user")
    payload = {
        "username": username,
        "password": "123456"  
    }

    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data.get("message") == "User registered successfully!"
    print(f"User '{username}' registered successfully.")

def test_register_user_already_exists():
    
    payload = {
        "username": "moran",  
        "password": "123456"
    }

    response = requests.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code == 409
    data = response.json()
    assert data.get("error") == "Username already exists"
