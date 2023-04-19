from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentManagementPatientViewSet,
    AppointmentManagementSurgeonViewSet,
)

router: DefaultRouter = DefaultRouter()
router.register(
    r"management/patient",
    AppointmentManagementPatientViewSet,
    basename="management_patient",
)
router.register(
    r"management/surgeon",
    AppointmentManagementSurgeonViewSet,
    basename="management_patient",
)

urlpatterns: list = router.urls
