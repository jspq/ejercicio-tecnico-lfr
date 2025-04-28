from rest_framework.routers import DefaultRouter
from core.views.address_viewset import AddressViewSet
from core.views.driver_viewset import DriverViewSet
from core.views.service_viewset import ServiceViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = router.urls