from rest_framework.routers import DefaultRouter

from .views import PatientProfileViewSet

router: DefaultRouter = DefaultRouter()
router.register(
    "",
    PatientProfileViewSet,
    basename="patient_profile",
)

urlpatterns: list = router.urls
