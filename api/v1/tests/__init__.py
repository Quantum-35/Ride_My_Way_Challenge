import unittest
import json

from app import create_app
from app.models import users

SIGNUP_URL = '/api/v1/auth/register'


class BaseTests (unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
    # initialize the models
        self.user_model = users

        self.test_user = data = {
                    "username": "quantum",
                    "email": "Quan@gma.com",
                    "address": "3343312",
                    "password": "12345678",
                    "confirm_password": "12345678",
                    "role": "driver"}
