from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Address


class AddressTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.address_url = reverse('address-list')

    def test_create_valid_address(self):
        data = {
            "street": "123 Calle Principal",
            "city": "Bogotá",
            "latitude": 4.7110,
            "longitude": -74.0721
        }
        response = self.client.post(self.address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.get().street, "123 Calle Principal")

    def test_create_invalid_latitude_address(self):
        data = {
            "street": "456 Calle Secundaria",
            "city": "Medellín",
            "latitude": 100.0,
            "longitude": -75.0
        }
        response = self.client.post(self.address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('latitude', response.data)

    def test_create_invalid_longitude_address(self):
        data = {
            "street": "789 Calle Terciaria",
            "city": "Cali",
            "latitude": 4.0,
            "longitude": -200.0
        }
        response = self.client.post(self.address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('longitude', response.data)

    def test_list_addresses(self):
        Address.objects.create(street="Calle 1", city="Bogotá", latitude=4.7, longitude=-74.0)
        Address.objects.create(street="Calle 2", city="Medellín", latitude=6.2, longitude=-75.5)

        response = self.client.get(self.address_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_address(self):
        address = Address.objects.create(street="Calle 1", city="Bogotá", latitude=4.7, longitude=-74.0)
        url = reverse('address-detail', args=[address.id])

        updated_data = {
            "street": "Calle Actualizada",
            "city": "Bogotá",
            "latitude": 4.8,
            "longitude": -74.1
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address.refresh_from_db()
        self.assertEqual(address.street, "Calle Actualizada")

    def test_delete_address(self):
        address = Address.objects.create(street="Calle 3", city="Cali", latitude=3.4, longitude=-76.5)
        url = reverse('address-detail', args=[address.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Address.objects.count(), 0)