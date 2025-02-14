from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/inventory', methods=['GET'])
def get_inventory():
    products = list(db.products.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products), 200

@app.route('/inventory', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    img = data.get('img')

    if not name or not category or not price or not img:
        return jsonify({"error": "Missing required fields"}), 400

    product = {
        "name": name,
        "category": category,
        "price": price,
        "img": img
    }

    result = db.products.insert_one(product)
    product["_id"] = str(result.inserted_id)

    return jsonify(product), 201

@app.route('/inventory/<product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.get_json()
    update_fields = {}

    if 'name' in data:
        update_fields['name'] = data['name']
    if 'category' in data:
        update_fields['category'] = data['category']
    if 'price' in data:
        update_fields['price'] = data['price']
    if 'img' in data:
        update_fields['img'] = data['img']

    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_fields})

    if result.matched_count == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product updated successfully"}), 200

@app.route('/inventory/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = db.products.delete_one({"_id": ObjectId(product_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4015)