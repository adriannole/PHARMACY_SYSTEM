import requests

BASE_URL = "http://localhost:4008"

def test_reset_cart_success():

    payload = {
        "username": "moran" 
    }

    response = requests.post(f"{BASE_URL}/reset_cart", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] in ["Cart reset successfully!", "Cart is already empty!"]

def test_reset_cart_user_not_found():
    
    payload = {
        "username": "non_existing_user"
    }

    response = requests.post(f"{BASE_URL}/reset_cart", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert data.get("error") == "User not found"
