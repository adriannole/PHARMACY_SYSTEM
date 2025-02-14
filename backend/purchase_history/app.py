from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.shopping_cart

@app.route('/purchase_history/<username>', methods=['GET'])
def get_purchase_history(username):
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    purchase_history = db.purchase_history.find({"username": username})
    history_list = list(purchase_history)

    return jsonify(history_list), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4014)