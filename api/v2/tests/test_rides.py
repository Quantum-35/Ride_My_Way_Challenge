from flask import json
from tests.base_test import BaseTests


RIDES_URL = '/api/v2/rides'


class TestRides(BaseTests):

    def test_user_can_post_ride(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        print(access_token)
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.post(RIDES_URL,
                                    data=json.dumps(self.test_ride_data),
                                    content_type='application/json',
                                    headers=headers)
        print(response.data)
        self.assertTrue(response.status_code == 201)
        expected = {'message': 'Ride Successfully Created'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

    