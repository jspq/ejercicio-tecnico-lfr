import math
from rest_framework.exceptions import ValidationError
import random
import string

def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        R = 6371 #Radio de la Tierra en km

        """Hacemos conversion de latitudes y longitudes de grados a radianes"""
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        """Aplicamos la la formula Haversine, esta formula nos ayuda para coordenadas geograficas"""
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance
    except Exception as e:
        raise ValidationError({"mensaje": f"Error calculating distance: {str(e)}"})

"""Conversion de minutos a una cadena de horas y minutos"""
def convert_minutes_to_hours_and_minutes(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours > 0:
        return f"{hours} hora{'s' if hours > 1 else ''} y {remaining_minutes} minuto{'s' if remaining_minutes != 1 else ''}"
    else:
        return f"{remaining_minutes} minuto{'s' if remaining_minutes != 1 else ''}"

"""Genera un codigo secreto aleatorio de letras y numeros para que el domiciliario tenga la opcion de validar
el usuario del servicio"""
def generate_secret_code(self, length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))