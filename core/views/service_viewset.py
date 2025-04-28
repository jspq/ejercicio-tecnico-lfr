from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from core.models import Service, Driver
from core.serializers.service_serializer import ServiceSerializer
from django.utils import timezone
from core.utils.util import calculate_distance, convert_minutes_to_hours_and_minutes, generate_secret_code


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    """Este parametro se puede escalar a futuro dandole un umbral de distancia permitida a cada
    ciudad ya que el tamaño de ciudad varia"""
    MAX_DISTANCE_KM = 20

    def create(self, request, *args, **kwargs):
        """Validamos los datos de entrada para poder extraer la direccion del servicio solicitado"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pickup_address = serializer.validated_data['pickup_address']

        """Hacemos el respectivo filtro de los conductores que se encuentren disponibles para
        prestar servicio, como tambien pertenezcan a la misma ciudad del servicio solicitado por el
        usuario"""
        available_drivers = Driver.objects.filter(
            is_available=True,
            current_address__city=pickup_address.city
        )

        """Validamos si existen conductores candidatos a prestar el servicio solicitado"""
        if not available_drivers.exists():
            raise ValidationError({"mensaje": "No hay conductores disponibles en estos momentos."})

        drivers_with_distance = []

        """Calculamos las distancias entre los conductores disponbiles y la direccion del servicio solicitado"""
        for driver in available_drivers:
            distance = calculate_distance(
                pickup_address.latitude,
                pickup_address.longitude,
                driver.current_address.latitude,
                driver.current_address.longitude
            )
            drivers_with_distance.append((driver, distance))

        """Aplicamos un orden por la distancia de menor a mayor"""
        drivers_with_distance.sort(key=lambda x: x[1])

        nearest_driver = None
        shortest_distance = None

        """Seleccionamos el conductor que se encuentre igual o por debajo del umbral de distancia parametrizado"""
        for driver, distance in drivers_with_distance:
            if distance <= self.MAX_DISTANCE_KM:
                nearest_driver = driver
                shortest_distance = distance
                break

        if nearest_driver is None:
            raise ValidationError({"mensaje": "No hay conductores cercanos a su ubicación."})

        """Calculamos el tiempo estimado del conductor seleccionado al lugar destino"""
        estimated_arrival_minutes = int(shortest_distance * 2)
        estimated_time = convert_minutes_to_hours_and_minutes(estimated_arrival_minutes)
        generated_secret_code = generate_secret_code(self)

        """Se crea el servicio con el conductor asignado"""
        service = serializer.save(
            driver=nearest_driver,
            status="ASSIGNED",
            estimated_arrival_time=estimated_arrival_minutes,
            secret_code=generated_secret_code,
        )

        """Se cambia el estado de disponibilidad del conductor a falso"""
        nearest_driver.is_available = False
        nearest_driver.save()

        return Response({
            "mensaje": "Servicio creado exitosamente.",
            "service_id": service.id,
            "assigned_driver": {
                "name": nearest_driver.name,
                "vehicle_model": nearest_driver.vehicle_model,
                "vehicle_color": nearest_driver.vehicle_color,
                "license_plate": nearest_driver.license_plate,
            },
            "secret_code": service.secret_code,
            "estimated_arrival_time": estimated_time,
            "pickup_address": {
                "latitude": pickup_address.latitude,
                "longitude": pickup_address.longitude,
                "address": pickup_address.street,
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        try:
            service = self.get_object()
        except Service.DoesNotExist:
            raise NotFound({"mensaje": "Servicio no encontrado."})

        if service.status != "ASSIGNED":
            return Response({"mensaje": "El servicio no se encuentra en progreso."}, status=status.HTTP_400_BAD_REQUEST)

        service.status = "COMPLETED"
        service.completed_at = timezone.now()
        try:
            service.save()
        except Exception as e:
            return Response({"mensaje": f"Ha ocurrido un error al completar el servicio: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        """Al completar el servicio tenemos que poner al conductor de nuevo en disponibilidad"""
        if service.driver:
            service.driver.is_available = True
            try:
                service.driver.save()
            except Exception as e:
                return Response({"mensaje": f"Ha ocurrido un error al actualizar el estado del conductor: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"mensaje": "Servicio completado exitosamente."}, status=status.HTTP_200_OK)