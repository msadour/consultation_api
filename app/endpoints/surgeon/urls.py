from rest_framework.routers import DefaultRouter

from .views import SurgeonAvailableViewSet, SurgeonTaskViewSet

router: DefaultRouter = DefaultRouter()
router.register(
    "",
    SurgeonAvailableViewSet,
    basename="surgeon_available",
)
router.register(
    "task",
    SurgeonTaskViewSet,
    basename="surgeon_task",
)

urlpatterns: list = router.urls
