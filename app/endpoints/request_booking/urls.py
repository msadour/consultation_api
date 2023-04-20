from rest_framework.routers import DefaultRouter

from .views import PatientAppointmentRequestViewSet, SurgeonAppointmentRequestViewSet

router: DefaultRouter = DefaultRouter()
router.register(
    r"management/patient",
    PatientAppointmentRequestViewSet,
    basename="management_patient",
)
router.register(
    r"management/surgeon",
    SurgeonAppointmentRequestViewSet,
    basename="management_surgeon",
)

urlpatterns: list = router.urls
