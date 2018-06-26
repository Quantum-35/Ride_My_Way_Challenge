import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class User():
    '''
    This Class Stores all the user Data in the db_Users list 
    '''

    primary_key = 0
    db_users = []

    def __init__(self, username, email, address, password):
        self.id = User.primary_key
        self.username = username
        self.email = email
        self.address = address
        self.password = generate_password_hash(password)
        User.primary_key += 1

    def save(self):
        user_detail = {}
        user_detail['id'] = User.primary_key
        user_detail['username'] = self.username
        user_detail['email'] = self.email
        user_detail['address'] = self.address
        user_detail['password'] = self.password
        User.db_users.append(user_detail)

    @staticmethod
    def encode_auth_token(user_email):

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                        days=current_app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                        seconds=current_app.config.get(
                        'AUTH_TOKEN_EXPIRY_SECONDS')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_email
            }
            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms='HS256')
            is_token_blacklisted = BlackListToken.check_blacklist(token)
            if is_token_blacklisted:
                return 'Token was Blacklisted, Please login In'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    @staticmethod
    def get_by_email(email):
        check_email = next(filter(lambda x: x['email'] == email, User.db_users), None)
        if check_email:
            return check_email

    def dicts(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password)


class BlackListToken:
    '''
    This Class stores tokens that are no longer valid.Every time a user logs out user 
    validation Token is stores in this class
    '''

    id = 0
    token_db = []
    blacklisted_on = []

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def blacklist(self):
        black = {}
        black['token'] = self.token
        black['time'] = self.blacklisted_on
        BlackListToken.token_db.append(black)

    @staticmethod
    def check_blacklist(token):
        check_token = next(filter(lambda x: x['token'] == token, BlackListToken.token_db), None)
        if check_token:
            return True
        return False


class Rides:
    '''
    Stores User Rides that can be easily retived or stored
    '''
    db_rides = []
    db_request = []
    ride_id = 1

    def __init__(self, origin, destination, car_model, driver_name, depature):
        self.id = Rides.ride_id
        self.origin = origin
        self.destination = destination
        self.car_model = car_model
        self.driver_name = driver_name
        self.depature = depature
        Rides.ride_id += 1

    def save(self):
        ride_detail = {}
        ride_detail['id'] = Rides.ride_id-1
        ride_detail['origin'] = self.origin
        ride_detail['destination'] = self.destination
        ride_detail['car_model'] = self.car_model
        ride_detail['driver_name'] = self.driver_name
        ride_detail['depature'] = self.depature
        Rides.db_rides.append(ride_detail)

    @classmethod
    def make_request(cls, rd_id):
        rd_req = {}
        rd_req['ride_requestid'] = rd_id
        Rides.db_rides.append(rd_req)

    def dicts(self):
        return dict(
            id=self.id,
            origin=self.origin,
            depature=self.depature,
            destination=self.destination,
            driver=self.driver_name,
            car_model=self.car_model)
