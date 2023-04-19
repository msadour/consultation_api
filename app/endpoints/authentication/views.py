from typing import Any

from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from app.endpoints.authentication.serializers import AuthTokenSerializer
from app.layer.exception import AuthenticationError


@permission_classes((permissions.AllowAny,))
class CustomAuthTokenView(ObtainAuthToken):

    authentication_classes: list = [TokenAuthentication]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: AuthTokenSerializer = AuthTokenSerializer()
        try:
            user_logged = serializer.validate(attrs=request.data)
            request.user = user_logged
            return Response(data={"token": request.user.auth_token.key}, status=201)
        except AuthenticationError as e:
            return Response(data={"error": str(e)}, status=400)


@permission_classes((permissions.AllowAny,))
class LogoutViewSet(viewsets.ViewSet):
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
