import re

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