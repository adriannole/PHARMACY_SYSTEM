from pymongo import MongoClient

client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart




db.products.delete_many({})

products = [
    # analgesic
    {"name": "Paracetamol", "category": "analgesic", "price": 6, "img": "/images/1.png"},
    {"name": "Paracetaol t2", "category": "analgesic", "price": 7, "img": "/images/2.png"},
    {"name": "Paracetamol x10", "category": "analgesic", "price": 8, "img": "/images/3.png"},
    {"name": "Paracetamol 100mg", "category": "analgesic", "price": 5, "img": "/images/4.png"},
    {"name": "Paracetamol 50mg", "category": "analgesic", "price": 4, "img": "/images/5.png"},

    # Antihypertensives
    {"name": "Tomato", "category": "Antihypertensives", "price": 6, "img": "/images/6.png"},
    {"name": "Cucumber", "category": "Antihypertensives", "price": 2.5, "img": "/images/7.png"},
    {"name": "Orange pepper", "category": "Antihypertensives", "price": 6, "img": "/images/8.png"},
    {"name": "Red pepper", "category": "Antihypertensives", "price": 7, "img": "/images/9.png"},
    {"name": "Yellow pepper", "category": "Antihypertensives", "price": 9, "img": "/images/10.png"},

    # Antiemetics
    {"name": "Chips", "category": "Antiemetics", "price": 6, "img": "/images/11.png"},
    {"name": "Cookies", "category": "Antiemetics", "price": 7, "img": "/images/12.png"},

    # Anti-inflammatory
    {"name": "Water", "category": "Anti-inflammatory", "price": 6, "img": "/images/13.png"},
    {"name": "Juice", "category": "Anti-inflammatory", "price": 5, "img": "/images/14.png"},
    {"name": "Soda", "category": "Anti-inflammatory", "price": 6, "img": "/images/15.png"},
    {"name": "Coffee", "category": "Anti-inflammatory", "price": 5.5, "img": "/images/16.png"},
    {"name": "Tea", "category": "Anti-inflammatory", "price": 5.5, "img": "/images/17.png"},

    # Antipyretics
    {"name": "Chicken", "category": "Antipyretics", "price": 3, "img": "/images/18.png"},
    {"name": "Beef", "category": "Antipyretics", "price": 4, "img": "/images/19.png"},
    {"name": "Fish", "category": "Antipyretics", "price": 6, "img": "/images/20.png"},
    {"name": "Sausage", "category": "Antipyretics", "price": 4.5, "img": "/images/21.png"},

    # Anti-allergy
    {"name": "Cheese", "category": "Anti-allergy", "price": 4, "img": "/images/22.png"},
    {"name": "Milk", "category": "Anti-allergy", "price": 6, "img": "/images/23.png"},
    {"name": "Butter", "category": "Anti-allergy", "price": 7, "img": "/images/24.png"},
    {"name": "Yogurt", "category": "Anti-allergy", "price": 2.5, "img": "/images/25.png"},

   
]

result = db.products.insert_many(products)

print(f"Inserted {len(result.inserted_ids)} products into the database.")

purchase_history = [
    {"username": "user1", "product_name": "Apple", "quantity": 3, "price": 6, "date": "2025-02-10"},
    {"username": "user1", "product_name": "Banana", "quantity": 2, "price": 2, "date": "2025-02-11"},
    {"username": "user2", "product_name": "Milk", "quantity": 1, "price": 4, "date": "2025-02-10"},
]

db.purchase_history.delete_many({})
db.purchase_history.insert_many(purchase_history)

print(f"Inserted {len(purchase_history)} purchase history records into the database.")
