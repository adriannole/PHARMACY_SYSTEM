from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS for everyone
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for everyone

# Connect to MongoDB
client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/reset_cart/<username>', methods=['POST'])
def reset_cart(username):
    user_cart = db.carts.find_one({"username": username})
    if not user_cart:
        return jsonify({"error": "Cart not found"}), 404

    db.carts.update_one({"username": username}, {"$set": {"products": []}})

    return jsonify({"message": "Cart reset"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4008)