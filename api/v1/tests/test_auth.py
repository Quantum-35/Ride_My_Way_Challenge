import unittest
from app import create_app
from flask import json

from tests import BaseTests

SIGNUP_URL = '/api/v1/auth/register'


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
        excpected = {'message': 'Enter correct email format'}
        self.assertEquals(excpected['message'],
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
        excpected = {'message': 'short password.Enter atleast 6 characters'}
        self.assertEquals(excpected, json.loads(response.data))
