import requests

BASE_URL = "http://localhost:4003"

def test_delete_product_success():
    
    username = "moran"
    product_name = "Apple"

    response = requests.delete(f"{BASE_URL}/delete_product", json={
        "username": username,
        "product_name": product_name
    })

    assert response.status_code == 200
    assert response.json().get("message") == "Product deleted successfully!"

def test_delete_product_user_or_product_not_found():
    
    username = "non_existing_user"
    product_name = "NonExistingProduct"

    response = requests.delete(f"{BASE_URL}/delete_product", json={
        "username": username,
        "product_name": product_name
    })

    assert response.status_code == 404
    assert response.json().get("error") == "Product not found in user's cart"
