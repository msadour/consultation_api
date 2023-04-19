from django.db import models

from app.endpoints.patient.models import Patient
from app.endpoints.surgeon.models import Surgeon


class Appointment(models.Model):

    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
