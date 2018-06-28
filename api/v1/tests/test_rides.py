from flask import json
from tests import BaseTests


RIDES_URL = '/api/v1/rides/'


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

    def test_user_can_post_and_fetch_single_ride(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200) 
        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.post('/api/v1/rides/',
                                    data=json.dumps(self.test_ride_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)
        response = self.client.get('/api/v1/rides/1',
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 200)
        expected = {'status': 'ok'}
        self.assertEquals(expected['status'], json.loads(response.data)['status'])

    def test_user_can_get_that_does_not_exist(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)

        response = self.login_user()
        self.assertTrue(response.status_code == 200)

        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))

        response = self.client.post(
                            '/api/v1/rides/12/requests',
                            data=json.dumps({
                                "pickup": "Nairobi",
                                "destination": "Nakuru",
                                "pickuptime": "122312"}),
                            headers=headers,
                            content_type='application/json')
        self.assertTrue(response.status_code == 404)
        expected = {'message': 'Riide with that id Does not exist'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        response = self.client.get('/api/v1/rides/1',
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 404)
        expected = {'message': 'Ride with that id Does not exist'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        response = self.client.post('/api/v1/rides/',
                                    data=json.dumps(self.test_ride_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)

        response = self.client.get('/api/v1/rides/11',
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 404)
        expected = {'message': 'Ride with that id Does not exist'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        response = self.client.post(
                            '/api/v1/rides/1/requests',
                            data=json.dumps({
                                "pickup": "Nairobi",
                                "destination": "Nakuru",
                                "pickuptime": "122312"}),
                            headers=headers,
                            content_type='application/json')
        print(response.data)
        self.assertTrue(response.status_code == 201)

        response = self.client.post(
                            '/api/v1/rides/12/requests',
                            data=json.dumps({
                                "pickup": "Nairobi",
                                "destination": "Nakuru",
                                "pickuptime": "122312"}),
                            headers=headers,
                            content_type='application/json')
        self.assertTrue(response.status_code == 404)
        expected = {'message': 'Ride with that id Does not exist'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])
