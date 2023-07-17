from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt
import jwt
import db_conn
from db_conn import *


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello RackTech"

@app.route('/register',methods=['POST'])
def register():
    body = request.json
    phone_num = body['number']
    email = body['email']
    password = body['password']
    company = body['company']
    # Check if the username is already registered
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return jsonify({
            "message": "Email address already exists"
        }), 409

    #Hashing password
    db_password = sha256_crypt.encrypt(password)

    #Validating credentials
    if phone_num == "" or email == "" or password == "":
        return jsonify({
            "message":"Error adding user"
        }),500
    else:
        document = {
            "username":email,
            "password":db_password,
            "phone":phone_num,
            "company":company
        }
        result = users_collection.insert_one(document)
        return jsonify(
            {
                "message":"User added successfully"
            }
        )

@app.route('/login',methods = ['POST'])
def login():
    body = request.json
    username = body['username']
    password = body['password']

    existing_user = users_collection.find_one({"username": username})
    if not existing_user:
        return jsonify({
            "message": "Username does not exist"
        }), 409
    document = users_collection.find_one({"username":username})
    if document:
        db_pass = document.get("password")
    if username != "" or password != "":
            if password:
                if username and sha256_crypt.verify(password,db_pass):
                    #Generating JWT Token
                    payload = {
                        "username":username,
                    }
                    secret_key = 'hv7$#VZ#3SyWU&Q9B@Yb#7e!DkfZ%*nJ'
                    token = jwt.encode(payload, secret_key, algorithm='HS256')
                    return {
                        "message":"Login Successfully",
                        "token" : token
                    }
                else:
                    return jsonify({"message": "Invalid username or password"}), 409
    else:
        return jsonify({"message": "Failed to login"}), 409

@app.route('/products')
def getProducts():
    category = request.args.get('category')
    products = list(db_conn.products_collection.find({'category': category}))
    serialized_products = []
    for product in products:
        serialized_products.append({
            'name':product['name'],
            'image':product['image'],
            'category':product['category']
        })
    return jsonify(serialized_products)



if __name__ == '__main__':
    app.run()
