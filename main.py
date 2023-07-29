from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt
from jwt_token import generate_token
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
            "email":email,
            "password":db_password,
            "phone":phone_num,
            "company":company
        }
        result = users_collection.insert_one(document)
        token = generate_token(email)
        return jsonify(
            {
                "message":"User added successfully",
                "token":token
            }
        )

@app.route('/login',methods = ['POST'])
def login():
    body = request.json
    email = body['email']
    password = body['password']

    existing_user = users_collection.find_one({"email": email})
    if existing_user==0:
        return jsonify({
            "message": "Email does not exist"
        }), 409
    document = users_collection.find_one({"email":email})
    print(document)
    db_pass = document["password"]
    if email != "" or password != "":
            if password:
                if email and sha256_crypt.verify(password,db_pass):
                    #Generating JWT Token
                    token = generate_token(email)
                    return jsonify(
                        {
                            "message": "Login Successfully",
                            "token": token
                        }
                    ),200
                else:
                    return jsonify({"message": "Invalid username or password"}), 409
    else:
        return jsonify({"message": "Failed to login"}), 409



@app.route('/products')
def getProducts():
    best_selling = request.args.get('best-seller')
    category = request.args.get('category')
    if best_selling == 'yes':
        products = list(db_conn.products_collection.find({'best-seller':best_selling}))
    if category:
        products = list(db_conn.products_collection.find({'category': category}))
    serialized_products = []
    for product in products:
        serialized_products.append({
            'name':product['name'],
            'image':product['image'],
            'description':product['description'],
            'category':product['category']
        })
    print(len(serialized_products))
    return jsonify(serialized_products)


@app.route('/profile')
def getProfile():
    email = request.args.get('email')
    print(email)
    user_details = users_collection.find_one({'email':email})
    email = user_details['email']
    phone = user_details['phone']
    company = user_details['company']
    return jsonify(
        {
            "email":email,
            "phone":phone,
            "company":company
        }
    ), 200

if __name__ == '__main__':
    app.run()
