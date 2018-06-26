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
        self.conn  = psycopg2.connect(host="localhost",database="test_andela", user="postgres", password="leah")
        create_tables()
        print('0000000',self.conn)
        self.test_user = {
                    "username": "quantum",
                    "email": "quanrum@gma.com",
                    "address": "3343312",
                    "password": "12345678",
                    "confirm_password": "12345678"}
    def tearDown(self):
        curs = self.conn.cursor()
        print('**********',curs)
        curs.execute('select * from users')
        row=curs.fetchone()
        print('555555555555555555555555555555555',row)
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