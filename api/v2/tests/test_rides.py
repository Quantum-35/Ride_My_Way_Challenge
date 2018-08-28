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
        response = self.client.post('/api/v2/users/rides',
                                    data=json.dumps(self.test_ride_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)
        expected = {'message': 'Ride Successfully Created'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])
        #test user posts empty rides

        response = self.client.get('/api/v2/users/ride',
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)
        
        response = self.client.post('/api/v2/users/rides',
                                    data = json.dumps({
                                        "car_model": "",
                                        "depature": "3343",
                                        "destination": "Limuru",
                                        "driver_name": "quantum",
                                        "origin": "kitale",
                                        'seats':'20'
                                    }),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 400)

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

        # User getting all rides ever joined
        response = self.client.get('/api/v2/users/rides/111000000000',
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 404)

        # Test for getting all ride requests

        response = self.client.get('/api/v2/requests',
                                  content_type='application/json',
                                  headers=headers)
        print(response.data)
        self.assertTrue(response.status_code == 404)

        

    def test_user_can_make_riderequests(self):
        response = self.register_user()
        self.assertTrue(response.status_code == 201)
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.post('/api/v2/users/rides',
                                    data=json.dumps(self.test_ride_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)
        expected = {'message': 'Ride Successfully Created'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])
        # Test ride that does not exist

        response = self.client.get('/api/v2/user/myrides',
                                    content_type='application/json',
                                    headers=headers)
        expected = {'message': 'You have never Joined any Ride request'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        
        response = self.client.delete('/api/v2/users/ride/2',
                                      content_type='application/json',
                                      headers=headers)
        self.assertTrue(response.status_code == 200) 
        
        response = self.register_user2()
        self.assertTrue(response.status_code == 201)
        response = self.login_user2()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))
        # Test for user making request to ride that exists
        response = self.client.get('/api/v2/rides',
                                    content_type='application/json',
                                    headers=headers)

        response = self.client.post('/api/v2/rides/1/requests',
                                    data=json.dumps(self.request_data),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)

        response = self.client.post('/api/v2/rides/1/requests',
                                    data=json.dumps({
                                        "pickup": "",
                                        "destination": "",
                                        "pickuptime": ""
                                    }),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 400)

        #Test for user accept ride request 

        response = self.client.put('/api/v2/rides/1/requests/1',
                                    data=json.dumps({"accepted": "True"}),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)

        # Test to accept rides that does not exist

        response = self.client.put('/api/v2/rides/1333/requests/1',
                                    data=json.dumps({"accepted": "True"}),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 404)

        #Test for user Does not accept ride request 

        response = self.client.put('/api/v2/rides/1/requests/1',
                                    data=json.dumps({"accepted": "false"}),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 201)
        expected = {'message': 'request successfully rejected'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        response = self.client.put('/api/v2/rides/1/requests/1',
                                    data=json.dumps({"accepted": ""}),
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)
        expected = {'message': 'you have not accepted request'}
        self.assertEquals(expected['message'], json.loads(response.data)['message'])

        response = self.client.get(RIDES_URL,
                                   content_type='application/json',
                                   headers=headers)
        self.assertTrue(response.status_code == 200)

        # Test for user fetching all requests to a ride offer

        response = self.client.get('/api/v2/users/rides/1/requests',
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 200)

        # Test for getting all ride requests

        response = self.client.get('/api/v2/requests',
                                  content_type='application/json',
                                  headers=headers)
        self.assertTrue(response.status_code == 404)

        response = self.client.get('/api/v2/users/rides/111/requests',
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 404)

        response = self.client.get('/api/v2/users/ride',
                                    content_type='application/json',
                                    headers=headers)
        self.assertTrue(response.status_code == 404)
        
        response = self.login_user()
        self.assertTrue(response.status_code == 200)
        access_token = json.loads(response.data)['token']
        headers = dict(Authorization='Bearer {}'.format(access_token))
        response = self.client.get('/api/v2/requests',
                                  content_type='application/json',
                                  headers=headers)
        self.assertTrue(response.status_code == 200)
