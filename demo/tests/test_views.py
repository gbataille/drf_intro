from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class SampleTest(APITestCase):

    def test_something(self):
        response = self.client.get(
            reverse('item-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.json())
