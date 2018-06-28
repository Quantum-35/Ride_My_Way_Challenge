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
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.post(RIDES_URL,
                                    data=json.dumps(self.test_ride_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)
        expected = {'message': 'Ride Successfully Created'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        # Test for user getting details of a single ride
        response = self.client.get('/api/v2/rides/1',
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 200)

        # Test for user trying to get details of ride that doesent exist
        response = self.client.get('/api/v2/rides/10000000000001',
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 404)
        expected = {'message': 'Ride with that id Does not exist'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        # Test for user making request to ride that exists
        response = self.client.post('/api/v2/rides/1/requests',
                                    data=json.dumps(self.request_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)

        # Test for user trying to make request to ride that does not exist
        response = self.client.post('/api/v2/rides/1000000000000/requests',
                                    data=json.dumps(self.request_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 404)
        expected = {'message': 'Ride with that id Does not exist'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        # Test for user fetching all requests to a ride offer
        response = self.client.get('/api/v2/rides/1/requests',
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)

        #Test for user accept ride request 
        response = self.client.put('/api/v2/rides/1/requests/1',
                                    data=json.dumps({"accepted": "True"}),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)

        #Test for user Does not accept ride request 
        response = self.client.put('/api/v2/rides/1/requests/1',
                                    data=json.dumps({"accepted": "NotTrue"}),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'you have not accepted request'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

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
        expected = {'status': 'ok'}
        self.assertTrue(expected['status'], json.loads(response.data)['status'])
        
    