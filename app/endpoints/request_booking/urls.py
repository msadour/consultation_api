from rest_framework.routers import DefaultRouter

from .views import PatientAppointmentRequestViewSet

router: DefaultRouter = DefaultRouter()
router.register(
    r"management/patient",
    PatientAppointmentRequestViewSet,
    basename="management_patient",
)

urlpatterns: list = router.urls
