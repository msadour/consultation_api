from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from app.layer.exception import AuthenticationError


class AuthTokenSerializer(serializers.Serializer):

    username: serializers.CharField = serializers.CharField()
    password: serializers.CharField = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def authenticate_user(
        self, email: str = None, password: str = None
    ) -> Optional[User]:
        user: User = get_user_model().objects.filter(email=email).first()

        if user is None:
            raise AuthenticationError("Not user found with this email.")

        if not user.is_active:
            raise AuthenticationError("This account is deactivate.")

        if not check_password(password, user.password):
            raise AuthenticationError("Email/Password doesn't match.")

        return user

    def validate(self, attrs: Any) -> User:
        if type(attrs) == QueryDict:
            attrs = attrs.dict()

        email: str = attrs.get("email")
        password: str = attrs.get("password")
        user: Optional[User] = self.authenticate_user(email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        user.auth_token = token

        return user
