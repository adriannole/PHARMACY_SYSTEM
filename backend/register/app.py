# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import jwt
from functools import wraps
import requests

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

client = MongoClient(
    "mongodb+srv://adrixer:arbolito@cluster0.paytk9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client.shopping_cart

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/123456/abcdef"  # Reemplaza con tu URL de webhook

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = db.users.find_one({"username": data['username']})
        except:
            return jsonify({"error": "Token is invalid!"}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    """
    Register NEW USER
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Check if the username already exists
        if db.users.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 409

        # Save the new user to the database
        hashed_password = generate_password_hash(password)
        user = {"username": username, "password": hashed_password, "cart": []}  # Add an empty cart
        db.users.insert_one(user)

        # Enviar correo de confirmación
        msg = Message("Registro Exitoso", recipients=[username])
        msg.body = f"Hola {username},\n\nRegistro exitoso."
        mail.send(msg)

        # Llamar al webhook
        webhook_data = {
            "username": username,
            "message": "Registro exitoso ."
        }
        requests.post(WEBHOOK_URL, json=webhook_data)

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4007)