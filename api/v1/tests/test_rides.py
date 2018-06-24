from flask import json
from tests import BaseTests


RIDES_URL = '/api/v1/rides'


class TestRides(BaseTests):

    def test_user_can_get_all_available_rides(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.get(RIDES_URL,
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 200)