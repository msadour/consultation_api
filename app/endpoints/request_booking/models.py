from django.db import models

from app.endpoints.patient.models import Patient
from app.endpoints.surgeon.models import Surgeon


class Status(models.TextChoices):

    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"


class RequestAppointment(models.Model):

    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    begin_at = models.TimeField()
    finish_at = models.TimeField()
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PENDING
    )

    objects = models.Manager()
