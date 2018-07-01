import json
from tests.base_test import BaseTests

SIGNUP_URL = '/api/v2/auth/register'
SIGNIN_URL = '/api/v2/auth/login'


class TestUserAuth(BaseTests):

    def test_user_send_get_request(self):
        response = self.client.get(SIGNUP_URL, content_type='application/json')
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'please Register'}
        self.assertEquals(expected['message'],
                          json.loads(response.data)['message'])

    def test_user_can_register(self):
        response = self.client.post(
            SIGNUP_URL,
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        print(response.data)
        self.assertTrue(response.status_code == 201)
        expected = {'message': 'Signed up successfully'}
        self.assertTrue(expected['message'], json.loads(response.data)['message'])
    
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
                    "username": "quantum Computing",
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
                    "username": "quantum computing",
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

    def test_user_login_with_invalid_wrong_password(self):
        self.register_user()
        response = self.client.post(SIGNIN_URL,
                                    data=json.dumps({
                                       "email": "mike@gma.com",
                                       "password": 'wrongpassword'}),
                                    content_type='application/json')
        print(response.data)
        self.assertTrue(response.status_code == 401)
        expected = {'message': 'Wrong username or password'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_login_with_valid_credantials(self):
        self.register_user()
        response = self.client.post(SIGNIN_URL,
                                    data=json.dumps({
                                       "email": "mike@gma.com",
                                       "password": '12345678'}),
                                    content_type='application/json')
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'Logged in successfully'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    def test_user_tries_to_access_route_without_token(self):
        response = self.client.get('/api/v2/rides',
                                    content_type='application/json')
        self.assertTrue(response.status_code == 400)
        expected = {'message': 'Ensure you have logged in and received a valid token'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    

    