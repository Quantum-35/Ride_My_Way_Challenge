import unittest
import json
import psycopg2

from app.app import create_app
from tests.create_testdb import create_tables

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
        self.test_user = {
                    "username": "quantum",
                    "email": "mike@gma.com",
                    "address": "3343312",
                    "password": "12345678",
                    "confirm_password": "12345678"}
    def tearDown(self):
        curs = self.conn.cursor()
        curs.execute('select * from users')
        row=curs.fetchone()
        curs.execute("DROP TABLE users")
        self.conn.commit()
        print(row)
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