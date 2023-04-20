from django.db import models
from django.conf import settings


class Surgeon(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="surgeon_user"
    )

    objects = models.Manager()

    USERNAME_FIELD = "email"
