import psycopg2
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash


# local import
from app.models import User
from app.auth.helpers import (email_validator,
                             address_validator,
                             password_validator,
                             user_name_validator,
                             token_required)

auth = Blueprint('auth', __name__)

'''
Route for Registering new users and throws valid error if the user exists
'''
@auth.route('/register', methods=['GET', 'POST'])
def user_auth():
    if request.method == 'POST':
        payload = request.get_json()
        username = payload['username']
        email = payload['email']
        address = payload['address']
        password = payload['password']
        conf_pass = payload['confirm_password']
        print(current_app.config['ENV']=='production')
        if username == '' or email == '' or \
           password == '' or address == '' or conf_pass == '':
            return jsonify({
                'message': "Failed you cannot submit empty fields",
                'status': 'failed'}), 400
        if not user_name_validator(username):
            return jsonify({
                'message': 'Wrong username Format',
                'status': 'failed'
            }), 400
        if not email_validator(email):
            return jsonify({
                'message': 'Enter correct email format',
                'status': 'failed'
            }), 400
        if not password_validator(password):
            return jsonify({
                'message': 'short password.Enter atleast 6 characters',
                'status': 'failed'}), 400

        if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        elif current_app.config['ENV']=='production':
            conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
        else:
            conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
        curs = conn.cursor()
        query = 'SELECT * FROM users WHERE email=%s'
        curs.execute(query, (email,))
        row = curs.fetchone()
        if not row:
            new_user = User(username, email, address, password)
            new_user.register_user()
            conn.close()
            print(current_app)
            print(current_app.config)
            return jsonify({
                'message': 'Signed up successfully',
                'status': 'ok'}), 201
        else:
            return jsonify({
                'message': 'User with that email exists',
                'status': 'failed'}), 403

    return jsonify({'message': 'please Register',
                    'status': 'ok'})

              
'''
Route for logging in the user and if the user does not exist a correct error is thrown
'''
@auth.route('/login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        payload = request.get_json()
        email = payload['email']
        password = payload['password']
        if not email_validator(email):
            return jsonify({
                'message': 'Wrong email format',
                'status': 'failed'
            }), 400
        if current_app.config['TESTING']:
            conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        else:
            conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
        curs = conn.cursor()
        query = 'SELECT * FROM users WHERE email=%s'
        curs.execute(query, (email,))
        row = curs.fetchone()
        if row:
            user_pass = row[4]
            if check_password_hash(user_pass, password):
                eml = row[2]
                token = User.encode_auth_token(user_email=eml).decode('utf-8')
                return jsonify({
                    'message': 'Logged in successfully',
                    'status': 'ok',
                    'token': token
                })
            else:
                return jsonify({
                    'message': 'Wrong username or password',
                    'status': 'failed'}), 401
        else:
            return jsonify({
                    'message': 'Wrong username or password',
                    'status': 'failed'}), 401
    return jsonify({
        'message': 'Please Login if already have an account',
        'status': 'success'})
