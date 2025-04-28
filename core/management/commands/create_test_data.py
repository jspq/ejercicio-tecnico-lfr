from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Address, Driver
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Crear direcciones y conductores de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker()

        if not User.objects.filter(username='test').exists():
            User.objects.create_user(
                username='test',
                email='testuser@example.com',
                password='test1234'
            )
            self.stdout.write(self.style.SUCCESS('Usuario de prueba creado correctamente'))
        else:
            self.stdout.write(self.style.WARNING('El usuario de prueba ya existe'))

        """Hay que hacer una direccion de referencia para generar direcciones que estén dentro
        del umbral de direcciones cercanas que es de 20KM y también superiores a 20KM"""
        base_latitude = 4.7110
        base_longitude = -74.0721

        addresses = []
        cities = ['Bogota', 'Medellin', 'Pereira', 'Armenia', 'Barranquilla', 'Ibague', 'Bucaramanga']

        """Direcciones que están en el umbral de 20 KM para conductores"""
        for _ in range(15):
            latitude_variation = random.uniform(-0.1, 0.1)  # pequeña variación
            longitude_variation = random.uniform(-0.1, 0.1)

            address = Address.objects.create(
                street=fake.street_address(),
                city=random.choice(cities),
                latitude=base_latitude + latitude_variation,
                longitude=base_longitude + longitude_variation
            )
            addresses.append(address)

        """Direcciones que están en el umbral de 20 KM para usuarios"""
        for _ in range(15):
            latitude_variation = random.uniform(-0.1, 0.1)  # pequeña variación
            longitude_variation = random.uniform(-0.1, 0.1)

            Address.objects.create(
                street=fake.street_address(),
                city=random.choice(cities),
                latitude=base_latitude + latitude_variation,
                longitude=base_longitude + longitude_variation
            )

        """Direcciones que están fuera del umbral de 20 KM para conductores"""
        for _ in range(15):
            latitude_variation = random.uniform(0.3, 1.0) * random.choice([-1, 1])  # variación mayor
            longitude_variation = random.uniform(0.3, 1.0) * random.choice([-1, 1])

            address = Address.objects.create(
                street=fake.street_address(),
                city=random.choice(cities),
                latitude=base_latitude + latitude_variation,
                longitude=base_longitude + longitude_variation
            )
            addresses.append(address)

        """Direcciones que están fuera del umbral de 20 KM para usuarios"""
        for _ in range(15):
            latitude_variation = random.uniform(0.3, 1.0) * random.choice([-1, 1])  # variación mayor
            longitude_variation = random.uniform(0.3, 1.0) * random.choice([-1, 1])

            address = Address.objects.create(
                street=fake.street_address(),
                city=random.choice(cities),
                latitude=base_latitude + latitude_variation,
                longitude=base_longitude + longitude_variation
            )
            addresses.append(address)

        vehicle_models = ['Toyota', 'BMW', 'Audi', 'Honda', 'Ford', 'Chevrolet', 'Nissan']
        vehicle_colors = ['Rojo', 'Azul', 'Negro', 'Blanco', 'Gris', 'Verde']

        for _ in range(60):
            random_address = random.choice(addresses)

            driver = Driver.objects.create(
                name=fake.name(),
                vehicle_model=random.choice(vehicle_models),
                vehicle_color=random.choice(vehicle_colors),
                license_plate=fake.bothify(text='???-###'),
                current_address=random_address,
                is_available=True,
                is_active=True
            )

        self.stdout.write(self.style.SUCCESS('Direcciones y conductores de prueba creados correctamente'))