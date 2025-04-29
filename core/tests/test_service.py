from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Service, Driver, Address


class ServiceCompletionTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.address = Address.objects.create(
            street="123 Main St",
            city="Test City",
            latitude=40.7128,
            longitude=-74.0060
        )

        self.driver = Driver.objects.create(
            name="Test Driver",
            current_address=self.address,
            vehicle_model="Toyota",
            vehicle_color="Rojo",
            license_plate="ABC-123",
            is_available=False
        )

        self.service = Service.objects.create(
            pickup_address=self.address,
            driver=self.driver,
            status="ASSIGNED",
            estimated_arrival_time=30
        )

    def test_complete_service_success(self):
        url = f'/api/services/{self.service.id}/complete/'
        response = self.client.post(url)

        self.service.refresh_from_db()
        self.assertEqual(self.service.status, "COMPLETED")
        self.assertIsNotNone(self.service.completed_at)

        self.driver.refresh_from_db()
        self.assertTrue(self.driver.is_available)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mensaje'], "Servicio completado exitosamente.")

    def test_complete_service_not_in_progress(self):
        self.service.status = "PENDING"
        self.service.save()

        url = f'/api/services/{self.service.id}/complete/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['mensaje'], "El servicio no se encuentra en progreso.")

    def test_complete_service_driver_not_assigned(self):
        service_no_driver = Service.objects.create(
            pickup_address=self.address,
            status="ASSIGNED",
            estimated_arrival_time=30
        )

        url = f'/api/services/{service_no_driver.id}/complete/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mensaje'], "Servicio completado exitosamente.")
        self.assertIsNone(service_no_driver.driver)
