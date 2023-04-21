from typing import Any

from django.contrib.auth import logout as django_logout
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.authentication.serializers import AuthTokenSerializer


class CustomAuthTokenView(ObtainAuthToken):

    authentication_classes: tuple = (TokenAuthentication,)
    permission_classes: tuple = (permissions.AllowAny,)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: AuthTokenSerializer = AuthTokenSerializer()
        user_logged: AbstractBaseUser = serializer.validate(attrs=request.data)
        request.user = user_logged
        return Response(data={"token": request.user.auth_token.key}, status=201)


class LogoutViewSet(viewsets.ViewSet):

    permission_classes: tuple = (permissions.IsAuthenticated,)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.user.auth_token.delete()
        django_logout(request)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
