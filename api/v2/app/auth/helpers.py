import re
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify, make_response, current_app

from app.models import User


def email_validator(email):
    """validates user provided email"""
    if re.match(
            "^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$",
            email):
        return True


def address_validator(address):
    """Handles the validation of address"""
    if re.match(
            '^[#.0-9a-zA-Z\s,-]+$',
            address):
        return True


def password_validator(password):
    """validates user provided password length"""
    if len(password) > 6:
        return True


def user_name_validator(username):
    """validates user provided username"""
    if re.match("^[a-zA-Z]*$", username):
        return True


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Provide a valiid auth token'
                })), 403

        if not token:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Token is missing'
            })), 401

        try:
            decode_response = User.decode_auth_token(token)
            if current_app.config['TESTING']:
                conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
            else:
                conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
            curs = conn.cursor()
            print(decode_response)
            query = 'SELECT * FROM users WHERE email=%s'
            curs.execute(query, (decode_response,))
            current_user = curs.fetchone()
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'failed',
                'message': message
            })), 401

        return f(current_user, *args, **kwargs)

    return decorated_function
