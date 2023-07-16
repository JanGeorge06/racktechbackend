from flask import Flask, request, jsonify,send_file
from passlib.hash import sha256_crypt
import jwt
from db_conn import *


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello RackTech"

@app.route('/register',methods=['POST'])
def register():
    body = request.json
    phone_num = body['number']
    user_name = body['username']
    password = body['password']

    # Check if the username is already registered
    existing_user = users_collection.find_one({"username": user_name})
    if existing_user:
        return jsonify({
            "message": "Username already exists"
        }), 409

    #Hashing password
    db_password = sha256_crypt.encrypt(password)

    #Validating credentials
    if phone_num == "" or user_name == "" or password == "":
        return jsonify({
            "message":"Error adding user"
        }),500
    else:
        document = {
            "username":user_name,
            "password":db_password,
            "phone":phone_num
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



if __name__ == '__main__':
    app.run()
