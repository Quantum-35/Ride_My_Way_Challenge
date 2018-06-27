import psycopg2
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app.create_tables import create_tables
from flask import current_app


# conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")


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
            
        else:
            self.conn  = psycopg2.connect(host="localhost",database="andela", user="postgres", password="leah")
            
    
    def register_user(self):
        create_tables()
        curs = self.conn.cursor()
        query = 'INSERT INTO users(username, email, address, password) VALUES(%s, %s, %s, %s)'
        curs.execute(query, (self.username, self.email, self.address, self.password))
        self.conn.commit()
        self.conn.close()

    
    def find_user_by_email(self, email):
        '''
        Fuction that finds user from the database by email
        '''
        create_tables()
        curs = self.conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        curs.execute(query, (email,))
        row = curs.fetchone()
        # if the user with that email exists
        if row:
            # if the data exists we create a user object with data from that row can be User(row[0], row[1], row[2], row[3])
            user = User(row[0], row[1], row[2], row[3])
        else:
            user = None
        return user

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
