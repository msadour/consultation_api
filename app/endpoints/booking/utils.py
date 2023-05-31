from datetime import datetime
from typing import Any

from django.db.models.query import QuerySet

from app.endpoints.booking.models import Appointment, Status
from app.endpoints.surgeon.models import Surgeon


def retrieve_future_appointments(current_user: Any, user_model: Any) -> QuerySet:
    current_date: datetime = datetime.now()
    if user_model == Surgeon:
        future_appointments: QuerySet = (
            Appointment.objects.filter(date__gte=current_date).filter(
                status=Status.BOOKED
            )
        ).filter(surgeon=current_user)
    else:
        future_appointments: QuerySet = (
            Appointment.objects.filter(date__gte=current_date).filter(
                status=Status.BOOKED
            )
        ).filter(patient=current_user)

    return future_appointments
