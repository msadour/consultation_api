from typing import Any, Optional

from django.http import QueryDict
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from app.layer.exception import AuthenticationError


class AuthTokenSerializer(serializers.Serializer):

    username: serializers.CharField = serializers.CharField()
    password: serializers.CharField = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def authenticate_user(
        self, email: str = None, password: str = None
    ) -> Optional[AbstractBaseUser]:
        user: AbstractBaseUser = get_user_model().objects.filter(email=email).first()

        if user is None:
            raise AuthenticationError("Not user found with this email.")

        if not user.is_active:
            raise AuthenticationError("This account is deactivate.")

        if not password == user.password:
            raise AuthenticationError("Email/Password doesn't match.")

        return user

    def validate(self, attrs: Any) -> AbstractBaseUser:
        if type(attrs) == QueryDict:
            attrs = attrs.dict()

        email: str = attrs.get("email")
        password: str = attrs.get("password")
        user: Optional[AbstractBaseUser] = self.authenticate_user(
            email=email, password=password
        )

        return user
