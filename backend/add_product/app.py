from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
#database connection
client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    username = data.get('username')
    product_name = data.get('product_name')
    quantity = data.get('quantity')

    if not username or not product_name or not quantity:
        return jsonify({"error": "Missing required fields"}), 400

    user_cart = db.carts.find_one({"username": username})
    if not user_cart:
        db.carts.insert_one({"username": username, "products": []})
        user_cart = db.carts.find_one({"username": username})

    product = db.products.find_one({"name": product_name})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart_products = user_cart["products"]
    for item in cart_products:
        if item["product_name"] == product_name:
            item["quantity"] += quantity
            break
    else:
        cart_products.append({"product_name": product_name, "quantity": quantity, "price": product["price"]})

    db.carts.update_one({"username": username}, {"$set": {"products": cart_products}})

    return jsonify({"message": "Product added to cart"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
