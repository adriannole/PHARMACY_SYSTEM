from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/get_cart/<username>', methods=['GET'])
def get_cart(username):
    user_cart = db.carts.find_one({"username": username})
    if not user_cart:
        return jsonify({"error": "Cart not found"}), 404

    return jsonify({"username": username, "cart": user_cart["products"]}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4005)