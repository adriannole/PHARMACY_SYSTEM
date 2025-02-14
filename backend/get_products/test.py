import requests

BASE_URL = "http://localhost:4012"

def test_get_products_with_category():

    category = "Fruits"

    response = requests.get(f"{BASE_URL}/get_products", params={"category": category})

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)  
    for product in products:
        assert product.get("category") == category  

def test_get_products_without_category():
    
    response = requests.get(f"{BASE_URL}/get_products")

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)  
    assert len(products) > 0  
    for product in products:
        assert "name" in product  
        assert "category" in product  
        assert "price" in product 
