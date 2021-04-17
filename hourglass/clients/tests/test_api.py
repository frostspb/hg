from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from hourglass.contrib.factories import ClientFactory, UserFactory


class ClientsTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(username='test')
        self.test_client = ClientFactory()
        self.client.force_authenticate(user=self.user)

    def test_clients(self):
        response = self.client.get(reverse('api:clients-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    'id': self.test_client.id,
                    'name': self.test_client.name,
                    'client_type': self.test_client.client_type,
                    'total_campaigns': self.test_client.total_campaigns,
                    'leads_generated': self.test_client.leads_generated,
                    'client_since': self.test_client.client_since,
                }
            ]
        )

        response = self.client.get(reverse('api:clients-detail', args=[self.test_client.id]), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
