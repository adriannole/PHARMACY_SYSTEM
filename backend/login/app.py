from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os
import jwt
import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(
    "mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client.shopping_cart

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        user = db.users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        print(f"Error accessing MongoDB: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4006)