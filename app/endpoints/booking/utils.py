from datetime import datetime
from typing import Any

from django.db.models.query import QuerySet

from app.endpoints.booking.models import Appointment, Status
from app.endpoints.surgeon.models import Surgeon


def retrieve_future_appointments(user_model: Any, current_user: Any) -> QuerySet:
    current_date: datetime = datetime.now()
    if user_model == Surgeon:
        future_appointments: QuerySet = (
            Appointment.objects.filter(surgeon=current_user)
            .filter(date__gte=current_date)
            .filter(status=Status.BOOKED)
        )
    else:
        future_appointments: QuerySet = (
            Appointment.objects.filter(patient=current_user)
            .filter(date__gte=current_date)
            .filter(status=Status.BOOKED)
        )
    return future_appointments
