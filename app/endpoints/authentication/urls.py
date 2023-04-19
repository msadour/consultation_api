from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomAuthTokenView, LogoutViewSet

router: DefaultRouter = DefaultRouter()
router.register(r"logout", LogoutViewSet, basename="logout")

urlpatterns: list = router.urls

urlpatterns += [path("login/", CustomAuthTokenView.as_view())]
