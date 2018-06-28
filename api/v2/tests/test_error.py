import json
from tests.base_test import BaseTests


class TestAppErrors(BaseTests):

    def test_404_error(self):
        response = self.client.get('/Deoes_nt_exist',
                                   content_type='application/json')
        self.assertTrue(response.status_code == 404)

    def test_405_error(self):
        response = self.client.put('/api/v2/auth/register',
                                   data=json.dumps(self.test_user),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 405)
