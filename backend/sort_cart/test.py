import requests

BASE_URL = "http://localhost:4010"

def test_sort_cart_success():
    
    payload = {
        "username": "moran"  
    }

    response = requests.post(f"{BASE_URL}/sort_cart", json=payload)

    assert response.status_code == 200
    sorted_cart = response.json()
    assert isinstance(sorted_cart, list)  

    for i in range(len(sorted_cart) - 1):
        assert sorted_cart[i]["total_price"] >= sorted_cart[i + 1]["total_price"]

def test_sort_cart_user_not_found():
    
    payload = {
        "username": "non_existing_user"  
    }

    response = requests.post(f"{BASE_URL}/sort_cart", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert data.get("error") == "Cart not found for the user"
