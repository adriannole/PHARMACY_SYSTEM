import requests

BASE_URL = "http://localhost:4005"

def test_get_cart_success():
    
    username = "moran"  

    response = requests.get(f"{BASE_URL}/get_cart/{username}")

    assert response.status_code == 200
    data = response.json()
    assert data.get("username") == username  
    assert isinstance(data.get("cart"), list)  

def test_get_cart_user_not_found():
    
    username = "non_existing_user"  

    response = requests.get(f"{BASE_URL}/get_cart/{username}")

    assert response.status_code == 404
    data = response.json()
    assert data.get("error") == "User not found"
