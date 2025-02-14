import requests

BASE_URL = "http://localhost:4009"

def test_search_products_by_category():
    
    query = "Fruits" 
    response = requests.get(f"{BASE_URL}/search_products", params={"query": query})

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)  
    for product in products:
        assert product.get("category") == query  

def test_search_products_no_query():
    
    response = requests.get(f"{BASE_URL}/search_products")

    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)  
    assert len(products) > 0  
    for product in products:
        assert "name" in product 
        assert "category" in product  
        assert "price" in product  
