from django.db import models
from django.core.exceptions import ValidationError


def validate_latitude(value):
    if not (-90 <= value <= 90):
        raise ValidationError(f"{value} is not a valid latitude.")


def validate_longitude(value):
    if not (-180 <= value <= 180):
        raise ValidationError(f"{value} is not a valid longitude.")


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    latitude = models.FloatField(validators=[validate_latitude])
    longitude = models.FloatField(validators=[validate_longitude])

    def __str__(self):
        return f"{self.street}, {self.city}"
