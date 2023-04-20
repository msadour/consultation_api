from django.db import models
from django.conf import settings

from app.layer.constants import SPECIALITIES


class Surgeon(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="surgeon_user"
    )
    specialty = models.CharField(
        max_length=255, choices=SPECIALITIES, default="Generalist"
    )

    objects = models.Manager()

    USERNAME_FIELD = "email"
