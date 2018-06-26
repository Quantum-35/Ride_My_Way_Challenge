import unittest

from app.auth.helper import (email_validator,
                             address_validator,
                             password_validator,
                             user_name_validator)


class TestHelper(unittest.TestCase):

    def test_wether_email_is_valid(self):
        self.assertTrue(email_validator('quantum@gmail.com'))

    def test_wether_address_is_valid(self):
        self.assertTrue(address_validator('123 Kitale'))

    def test_password_is_valid(self):
        self.assertTrue(password_validator('Hello World'))

    def test_user_name_is_valid(self):
        self.assertTrue(user_name_validator('Quantum'))
