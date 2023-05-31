from datetime import datetime
from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet

from app.endpoints.booking.models import Appointment, Status


def retrieve_future_appointments(current_user: Any) -> QuerySet:
    current_date: datetime = datetime.now()
    future_appointments: QuerySet = (
        Appointment.objects.filter(date__gte=current_date).filter(status=Status.BOOKED)
    ).filter(Q(surgeon=current_user) | Q(patient=current_user))
    return future_appointments
