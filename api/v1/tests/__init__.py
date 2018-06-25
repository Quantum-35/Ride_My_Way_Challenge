import unittest
import json

from app import create_app
from app.models import User

SIGNUP_URL = '/api/v1/auth/register'
SIGNIN_URL = '/api/v1/auth/login'


class BaseTests (unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
    # initialize the models
        self.user_model = User.db_users

        self.test_user = {
                    "username": "quantum",
                    "email": "Quan@gma.com",
                    "address": "3343312",
                    "password": "12345678",
                    "confirm_password": "12345678",
                    "role": "driver"}
        self.test_ride_data = {
            "car_model": "Mazda",
            "depature": "3343",
            "destination": "Nakuru",
            "driver_name": "quantum",
            "origin": "kitale"
        }

    def tearDown(self):
        self.user_model.clear()

    def register_user(self):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            SIGNUP_URL,
            data=json.dumps(self.test_user),
            content_type='application/json',)

    def login_user(self):
        self.register_user()
        return self.client.post(
            SIGNIN_URL,
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
