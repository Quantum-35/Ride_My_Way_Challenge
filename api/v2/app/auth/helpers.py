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
    if re.match("^([a-zA-Z]{2,}\\s[a-zA-z]{1,}'?-?[a-zA-Z]{2,}\\s?([a-zA-Z]{1,})?)", username):
        return True


def token_required(f):
    '''checks user have valid tokens'''
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization', None)
            access_token = auth_header.split(' ')[1]
            if access_token:
                decode_response = User.decode_auth_token(access_token)
                if current_app.config['TESTING']:
                    conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
                else:
                    conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
                curs = conn.cursor()
                query = 'SELECT * FROM users WHERE email=%s'
                curs.execute(query, (decode_response,))
                current_user = curs.fetchone()
                return f(current_user, *args, **kwargs)
            return jsonify({'message':"Please login first, your session might have expired"}), 401
        except Exception as e:
            return jsonify({'message': 'Ensure you have logged in and received a valid token'}),400
    return decorated