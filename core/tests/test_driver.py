from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from core.models import Driver, Address


class DriverModelTests(APITestCase):

    def setUp(self):
        self.address = Address.objects.create(
            street="Calle 123",
            city="Bogotá",
            latitude=4.7110,
            longitude=-74.0721
        )

    def test_create_driver(self):
        driver = Driver.objects.create(
            name="Juan Pérez",
            vehicle_model="Toyota Corolla",
            vehicle_color="Rojo",
            license_plate="ABC-123",
            current_address=self.address,
            is_available=True,
            is_active=True
        )
        self.assertEqual(driver.name, "Juan Pérez")
        self.assertEqual(driver.vehicle_model, "Toyota Corolla")
        self.assertTrue(driver.is_available)
        self.assertTrue(driver.is_active)
        self.assertEqual(driver.current_address, self.address)

    def test_driver_str_representation(self):
        driver = Driver.objects.create(
            name="Pedro Sánchez",
            vehicle_model="Ford Fiesta",
            vehicle_color="Azul",
            license_plate="XYZ-789",
            current_address=self.address
        )
        self.assertEqual(str(driver), "Pedro Sánchez")


class DriverAPITests(APITestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.address = Address.objects.create(
            street="Carrera 45",
            city="Medellín",
            latitude=6.2442,
            longitude=-75.5812
        )

    def test_list_drivers(self):
        Driver.objects.create(
            name="Camila Gómez",
            vehicle_model="Honda Civic",
            vehicle_color="Negro",
            license_plate="CDE-456",
            current_address=self.address
        )

        url = reverse('driver-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_driver(self):
        url = reverse('driver-list')
        data = {
            "name": "Carlos Ruiz",
            "vehicle_model": "Chevrolet Spark",
            "vehicle_color": "Blanco",
            "license_plate": "FGH-789",
            "current_address": self.address.id,
            "is_available": True,
            "is_active": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Driver.objects.count(), 1)
        self.assertEqual(Driver.objects.first().name, "Carlos Ruiz")

    def test_retrieve_driver(self):
        driver = Driver.objects.create(
            name="Ana Torres",
            vehicle_model="Nissan Sentra",
            vehicle_color="Gris",
            license_plate="JKL-012",
            current_address=self.address
        )

        url = reverse('driver-detail', args=[driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Ana Torres")

    def test_update_driver(self):
        driver = Driver.objects.create(
            name="Santiago Muñoz",
            vehicle_model="BMW X5",
            vehicle_color="Azul",
            license_plate="MNO-345",
            current_address=self.address
        )

        url = reverse('driver-detail', args=[driver.id])
        data = {
            "name": "Santiago Actualizado",
            "vehicle_model": "BMW X5",
            "vehicle_color": "Azul",
            "license_plate": "MNO-345",
            "current_address": self.address.id,
            "is_available": False,
            "is_active": True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        driver.refresh_from_db()
        self.assertEqual(driver.name, "Santiago Actualizado")
        self.assertFalse(driver.is_available)

    def test_delete_driver(self):
        driver = Driver.objects.create(
            name="Laura Vélez",
            vehicle_model="Audi A3",
            vehicle_color="Rojo",
            license_plate="PQR-678",
            current_address=self.address
        )

        url = reverse('driver-detail', args=[driver.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Driver.objects.count(), 0)