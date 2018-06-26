import re
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash


# local import
from app.models import User, BlackListToken
from app.auth.helper import (email_validator,
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
        user = User.get_by_email(email=email)
        if not user:
            reg_user = User(username=username,
                            email=email,
                            address=address,
                            password=password)
            reg_user.save()
            return jsonify({
                'message': 'signed up successfully {}'.format(reg_user.dicts()),
                'status': 'ok'}), 201
        else:
            return jsonify({
                'message': 'User with that email exists',
                'status': 'ok'}), 403

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
        check_email = User.get_by_email(email=email)
        if check_email:
            user_pass = User.db_users[0]['password']
            if check_password_hash(user_pass, password):
                eml = check_email['email']
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

'''
Route for logging out the user and blacklisting their tokens
'''
@auth.route('/logout', methods=['POST'])
@token_required
def handle_logout(current_user):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        decoded_token_response = User.decode_auth_token(auth_token)
        if not isinstance(decoded_token_response, str):
            token = BlackListToken(auth_token)
            token.blacklist()
            return jsonify({
                    'message': 'Successfully logged out',
                    'status': 'ok'}), 200
        return jsonify({
                        'message': decoded_token_response,
                        'status': 'failed'}), 401
    return jsonify({
                    'Message': 'Provide an authorization header',
                    'status': 'ok'}), 403
