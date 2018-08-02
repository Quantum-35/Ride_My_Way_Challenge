import psycopg2
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app.create_tables import create_tables, create_rides, create_requests
from flask import current_app


class User:
    '''
    This class persists user data to the database
    '''

    def __init__(self, username, email, address, password):
        self.username = username
        self.email = email
        self.address = address
        self.password = generate_password_hash(password)
        if current_app.config['TESTING']:
            self.conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        else :
            self.conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")    
        # else:
        #     self.conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
            
    
    def register_user(self):
        create_tables()
        curs = self.conn.cursor()
        query = 'INSERT INTO users(username, email, address, password) VALUES(%s, %s, %s, %s)'
        curs.execute(query, (self.username, self.email, self.address, self.password))
        self.conn.commit()
        self.conn.close()


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
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'



class Rides:
    
    def __init__(self, user_id,origin, destination, car_model, driver_name, depature, seats):
        self.origin = origin
        self.destination = destination
        self.car_model = car_model
        self.driver_name = driver_name
        self.depature = depature
        self.user_id = user_id
        self.seats = seats
        if current_app.config['TESTING']:
            self.conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
            
        else :
            self.conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
            
    def save_ride(self):
        create_rides()
        curs = self.conn.cursor()
        query = 'INSERT INTO ride(user_id, origin, destination, car_model, driver_name, depature, seats) VALUES(%s,%s, %s, %s, %s, %s, %s)'
        curs.execute(query, (self.user_id, self.origin, self.destination, self.car_model, self.driver_name, self.depature, self.seats))
        self.conn.commit()
        self.conn.close()

class Requests:
    
    accepted = 'False'
    def __init__(self, user_id,ride_id, user_req, pickup, destination, pickuptime, accepted='false'):
        self.user_id = user_id
        self.ride_id = ride_id
        self.user_req = user_req
        self.pickup = pickup
        self.destination = destination
        self.pickuptime = pickuptime
        self.accepted = accepted
        if current_app.config['TESTING']:
            self.conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
            
        else :
            self.conn  = psycopg2.connect(host="ec2-54-227-247-225.compute-1.amazonaws.com",
                                database="d59bsstdnueu2j", user="evmawfgeuwoycc", password="51bf40de92130e038cef26d265e51c504b62bb8449d48f4794c1da44bb69a947")
            
    def save_request(self):
        create_requests()
        curs = self.conn.cursor()
        query = 'INSERT INTO requests(user_id, ride_id, user_requested_id, pickup, destination, pickuptime, accepted) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        curs.execute(query, (self.user_id, self.ride_id, self.user_req, self.pickup, self.destination, self.pickuptime, self.accepted))
        self.conn.commit()
        self.conn.close()