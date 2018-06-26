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
            conn  = psycopg2.connect(host="localhost",database="test_andela", user="postgres", password="leah")
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
            return jsonify({
                'message': 'Signed up successfully',
                'status': 'ok'}), 201
        else:
            return jsonify({
                'message': 'User with that email exists',
                'status': 'failed'}), 403

    return jsonify({'message': 'please Register',
                    'status': 'ok'})
