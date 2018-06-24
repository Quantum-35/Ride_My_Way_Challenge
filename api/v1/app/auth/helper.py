import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify

from app.models import users,User

def email_validator(email):
    '''validates user provided email'''
    if re.match(
            "^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$",
            email):
        return True
def address_validator(address):
    '''Handles the validation of address'''
    if re.match(
            '^[#.0-9a-zA-Z\s,-]+$',
            address):
        return True

def password_validator(password):
    '''validates user provided password length'''
    if len(password) > 6:
        return True
def user_name_validator(username):
    '''validates user provided username'''
    if re.match("^[a-zA-Z]*$", username):
        return True

def token_required(f):
    '''checks user have valid tokens'''
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization', None)
            access_token = auth_header.split(' ')[1]
            if access_token:
                email = User.decode_auth_token(access_token)
                current_user = User.get_by_email(email=email)
                return f(current_user, *args, **kwargs)
            return jsonify({'message':"Please login first, your session might have expired"}), 401
        except Exception as e:
            return jsonify({'message': 'Ensure you have logged in and received a valid token', 'error':str(e)}),400
    return decorated