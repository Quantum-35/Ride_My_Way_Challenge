import time
import unittest
from app import create_app
from flask import json

from tests import BaseTests

SIGNUP_URL = '/api/v1/auth/register'
SIGNIN_URL = '/api/v1/auth/login'
LOGOUT_URL = '/api/v1/auth/logout'


class TestAuthentication (BaseTests):

    def test_user_send_get_request(self):
        response = self.client.get(SIGNUP_URL, content_type='application/json')
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'please Register'}
        self.assertEquals(expected['message'],
                          json.loads(response.data)['message'])

    def test_user_send_post_registration(self):
        response = self.client.post(
            SIGNUP_URL,
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        self.assertTrue(response.status_code == 201)
        expected = {'status': 'ok'}
        self.assertEquals(expected['status'],
                          json.loads(response.data)['status'])

    def test_user_send_post_registration_empty_fields(self):
        response = self.client.post(SIGNUP_URL, data=json.dumps({
                    "username": "",
                    "email": "",
                    "address": "",
                    "password": "",
                    "confirm_password": "",
                    "role": ""}),
                    content_type='application/json')
        self.assertTrue(response.status_code == 400)
        expected = {'message': 'Failed you cannot submit empty fields'}
        self.assertEquals(expected['message'],
                          json.loads(response.data)['message'])

    def test_user_send_post_registration_incorrect_email_format(self):
        response = self.client.post(SIGNUP_URL, data=json.dumps({
                    "username": "quantum",
                    "email": "quan",
                    "address": "122kitale",
                    "password": "12345678",
                    "confirm_password": "12345678",
                    "role": "driver"}),
                    content_type='application/json')
        self.assertTrue(response.status_code == 400)
        expected = {'message': 'Enter correct email format'}
        self.assertEquals(expected['message'],
                          json.loads(response.data)['message'])

    def test_user_send_post_registration_short_password(self):
        response = self.client.post(SIGNUP_URL, data=json.dumps({
                    "username": "quantum",
                    "email": "quan@gmail.com",
                    "address": "122kitale",
                    "password": "1",
                    "confirm_password": "1",
                    "role": "driver"}),
                    content_type='application/json')
        self.assertTrue(response.status_code == 400)
        expected = {'message': 'short password.Enter atleast 6 characters'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_post_invalid_username(self):
        response = self.client.post(SIGNUP_URL, data=json.dumps({
                    "username": "1u@",
                    "email": "quan@gmail.com",
                    "address": "122kitale",
                    "password": "1Hellowrodl",
                    "confirm_password": "1Hellowrodl"}),
                    content_type='application/json')
        self.assertTrue(response.status_code == 400)
        expected = {'message': 'Wrong username Format'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_post_user_already_registerd(self):
        self.register_user()
        response = self.client.post(SIGNUP_URL, data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertTrue(response.status_code == 403)
        expected = {'message': 'User with that email exists'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_send_get_login(self):
        response = self.client.get(SIGNIN_URL,
                                   content_type='application/json')
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'Please Login if already have an account'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_login_with_wrong_email_format(self):
        response = self.client.post(SIGNIN_URL,
                                    data=json.dumps({
                                       "email": "quangmailcom",
                                       "password": 'Quanajajsajssajs'}),
                                    content_type='application/json')
        self.assertTrue(response.status_code == 400)
        expected = {'message': 'Wrong email format'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_login_with_invalid_valid_credantials(self):
        self.register_user()
        response = self.client.post(SIGNIN_URL,
                                    data=json.dumps({
                                       "email": "Quant@gma.com",
                                       "password": '12345678'}),
                                    content_type='application/json')
        print(response.data)
        self.assertTrue(response.status_code == 401)
        expected = {'message': 'Wrong username or password'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_login_with_valid_credantials(self):
        self.register_user()
        response = self.client.post(SIGNIN_URL,
                                    data=json.dumps({
                                       "email": "Quan@gma.com",
                                       "password": '12345678'}),
                                    content_type='application/json')
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'Logged in successfully'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_valid_user_logout(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.post(LOGOUT_URL,
                                    content_type='application/json',
                                    headers=headers)
        expected = {'message': 'Quan@gma.com'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_expired_user_token(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        # Pause for 3 seconds
        time.sleep(self.app.config['AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS'])
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.post(LOGOUT_URL,
                                    content_type='application/json',
                                    headers=headers)
        expected = {'message': 'Signature expired, Please sign in again'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_invalid_user_token(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        headers = dict(Authorization='Bearer {}'.format('This is not a valid token'))
        response = self.client.post(LOGOUT_URL,
                                    content_type='application/json',
                                    headers=headers)
        expected = {'message': 'Invalid token. Please sign in again'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_without_header_token(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        response = self.client.post(LOGOUT_URL,
                                    content_type='application/json')
        expected = {'message': 'Token is missing'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])
