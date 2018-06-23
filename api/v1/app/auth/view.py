import re
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

# local import
from app.models import users

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
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({
                'message': 'Enter correct email format',
                'status': 'failed'}), 400
        if len(str(password)) < 6:
            return jsonify({
                'message': 'short password.Enter atleast 6 characters'}), 400
        user_details = {}
        user_details['username'] = username
        user_details['email'] = email
        user_details['address'] = address
        user_details['password'] = password
        users.append(user_details)
        return jsonify({
            'message': 'signed up successfully {}'.format(user_details),
            'status': 'ok'}), 201

    return jsonify({'message': 'please Register',
                    'status': 'ok'})
