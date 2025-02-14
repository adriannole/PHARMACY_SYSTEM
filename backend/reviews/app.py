from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/reviews', methods=['GET'])
def get_reviews():
    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    reviews = list(db.reviews.find({"product_id": product_id}))
    for review in reviews:
        review["_id"] = str(review["_id"])
    return jsonify(reviews), 200

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    product_id = data.get('product_id')
    username = data.get('username')
    rating = data.get('rating')
    comment = data.get('comment')

    if not product_id or not username or not rating or not comment:
        return jsonify({"error": "Missing required fields"}), 400

    review = {
        "product_id": product_id,
        "username": username,
        "rating": rating,
        "comment": comment
    }

    result = db.reviews.insert_one(review)
    review["_id"] = str(result.inserted_id)

    return jsonify(review), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4016)