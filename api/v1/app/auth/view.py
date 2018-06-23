import re
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash



# local import
from app.models import users
from app.auth.helper import (email_validator,
                             address_validator,
                             password_validator,
                             user_name_validator)

auth = Blueprint('auth', __name__)


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
        check_email = [e for e in users if e['email'] == email]
        if check_email:
            return jsonify({
                'message': 'User with that email exists',
                'status': 'ok'}), 403
        else:
            user_details = {}
            user_details['username'] = username
            user_details['email'] = email
            user_details['address'] = address
            user_details['password'] = generate_password_hash(password)
            users.append(user_details)
            return jsonify({
                'message': 'signed up successfully {}'.format(users),
                'status': 'ok'}), 201

    return jsonify({'message': 'please Register',
                    'status': 'ok'})


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
        check_email = [e for e in users if e['email'] == email]
        
        if check_email:
            user_pass = check_email[0].get('password')
            if check_password_hash(user_pass, password):
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=current_app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                                                                       seconds=current_app.config.get(
                                                                           'AUTH_TOKEN_EXPIRY_SECONDS')),
                    'iat': datetime.utcnow(),
                    'sub': check_email[0]['email']}
                token = jwt.encode(
                        payload,
                        current_app.config.get('SECRET_KEY'),
                        algorithm='HS256').decode('utf-8')
                return jsonify({
                    'message': 'Logged in successfully',
                    'status': 'ok',
                    'token': token
                })
        else:
          return jsonify({
                'message': 'Wrong username or password',
                'status': 'failed'
            }), 401  
    return jsonify({
        'message': 'Please Login if already have an account',
        'status': 'success'
    })

