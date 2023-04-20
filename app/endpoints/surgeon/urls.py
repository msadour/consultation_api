from rest_framework.routers import DefaultRouter

from .views import SurgeonAvailableViewSet

router: DefaultRouter = DefaultRouter()
router.register(
    "",
    SurgeonAvailableViewSet,
    basename="surgeon_available",
)

urlpatterns: list = router.urls
