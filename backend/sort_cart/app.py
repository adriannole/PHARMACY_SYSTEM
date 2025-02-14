from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/sort_cart/<username>', methods=['POST'])
def sort_cart(username):
    """
    Sort the user's cart items by total price (price * quantity) in descending order.
    """
    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Fetch the user's cart
    user_cart = db.carts.find_one({"username": username})
    if not user_cart:
        return jsonify({"error": "Cart not found for the user"}), 404

    cart_items = user_cart["products"]

    # Enrich the cart items with product details and calculate total price
    enriched_cart = []
    for item in cart_items:
        product = db.products.find_one({"name": item["product_name"]})
        if product:
            total_price = product["price"] * item["quantity"]
            enriched_cart.append({
                "product_name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"],
                "total_price": total_price,
            })
        else:
            enriched_cart.append({
                "product_name": item["product_name"],
                "price": 0,
                "quantity": item["quantity"],
                "total_price": 0,
            })

    # Sort the cart items by total price in descending order
    sorted_cart = sorted(enriched_cart, key=lambda x: x["total_price"], reverse=True)

    # Update the user's cart with the sorted items
    db.carts.update_one({"username": username}, {"$set": {"products": sorted_cart}})

    return jsonify({"message": "Cart sorted by price"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4010)