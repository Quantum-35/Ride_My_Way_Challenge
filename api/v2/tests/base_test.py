import unittest
import json
import psycopg2

from app.app import create_app
from tests.create_testdb import create_tables, create_rides

SIGNUP_URL = '/api/v2/auth/register'
SIGNIN_URL = '/api/v2/auth/login'


class BaseTests (unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.conn  = psycopg2.connect(host="localhost",database="test_rides", user="foo", password="bar")
        create_tables()
        create_rides()
        self.test_user = {
                    "username": "quantum",
                    "email": "mike@gma.com",
                    "address": "3343312",
                    "password": "12345678",
                    "confirm_password": "12345678"}

        self.test_ride_data = {
            "car_model": "Mazda",
            "depature": "3343",
            "destination": "Nakuru",
            "driver_name": "quantum",
            "origin": "kitale"}

    def tearDown(self):
        curs = self.conn.cursor()
        curs.execute('select * from users')
        curs.execute("DROP TABLE users CASCADE")
        curs.execute("DROP TABLE ride ")
        self.conn.commit()
        self.conn.close()

    def register_user(self):
        '''
        Helper method for registering users
        '''
        return self.client.post(
            SIGNUP_URL,
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
    def login_user(self):
        self.register_user()
        return self.client.post(
            SIGNIN_URL,
            data=json.dumps(self.test_user),
            content_type='application/json'
        )