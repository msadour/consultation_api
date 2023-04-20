from datetime import datetime, timedelta, time

from django.db.models.query import QuerySet
from django.db.models import Q

from app.endpoints.booking.models import Appointment
from app.endpoints.patient.models import Patient
from app.endpoints.request_booking.models import RequestAppointment, Status
from app.endpoints.surgeon.models import Surgeon
from app.layer.exception import WrongActionError, WrongDayError


def check_10_minutes_around_appointment(
    appointments_surgeon: QuerySet, begin_at: datetime, finish_at: datetime
):
    def _add_delta(
        tme: datetime.time, delta: timedelta, operande: str
    ) -> datetime.time:
        if operande == "-":
            return (datetime.combine(datetime.today(), tme) - delta).time()
        else:
            return (datetime.combine(datetime.today(), tme) + delta).time()

    finish_at_plus_10m: datetime.time = _add_delta(
        finish_at, timedelta(minutes=10), operande="+"
    )
    begin_at_minus_10m: datetime.time = _add_delta(
        begin_at, timedelta(minutes=10), operande="-"
    )
    query_10_minutes_around_appointment: bool = appointments_surgeon.filter(
        Q(begin_at__gte=finish_at_plus_10m) | Q(finish_at__lte=begin_at_minus_10m)
    ).exists()
    return not query_10_minutes_around_appointment


def get_appointments_requested(
    surgeon: Surgeon, patient: Patient, request_appointments: list
):
    appointments_requested: list = []

    appointment: dict
    for appointment in request_appointments:
        date_str: str = appointment["date"]
        date: datetime = datetime.strptime(date_str, "%Y-%m-%d")

        begin_at_str: str = appointment["begin_at"]
        begin_at: datetime = datetime.strptime(begin_at_str, "%H:%M")
        if (
            time(9, 00) > begin_at.time()
            or begin_at.time() > time(14, 15)
            or date.weekday() > 4
        ):
            continue

        finish_at: datetime = begin_at + timedelta(minutes=45)
        appointment.update({"finish_at": finish_at, surgeon: surgeon, patient: patient})
        appointments_requested.append(appointment)

    return [
        RequestAppointment(
            surgeon=surgeon,
            patient=patient,
            date=appointment_available.get("date"),
            begin_at=appointment_available.get("begin_at"),
            finish_at=appointment_available.get("finish_at"),
        )
        for appointment_available in appointments_requested
    ]


def update_appointment_request(request_appointment: RequestAppointment, action: str):
    if action == "confirm":
        date = request_appointment.date
        begin_at = request_appointment.begin_at
        finish_at = request_appointment.finish_at
        surgeon = request_appointment.surgeon
        patient = request_appointment.patient

        appointments_surgeon: QuerySet = Appointment.objects.filter(
            surgeon=surgeon
        ).filter(date=date)

        is_appointment_already_exist: bool = appointments_surgeon.filter(
            date=date
        ).exists()

        if (
            is_appointment_already_exist is False
            and check_10_minutes_around_appointment(
                appointments_surgeon=appointments_surgeon,
                begin_at=begin_at,
                finish_at=finish_at,
            )
        ):
            Appointment.objects.create(
                surgeon=surgeon,
                patient=patient,
                date=date,
                begin_at=begin_at,
                finish_at=finish_at,
            )
            request_appointment.status = Status.ACCEPTED
            request_appointment.save()
        else:
            raise WrongDayError(
                "You cannot have multiple appointment on the same day, or around 10 minutes of an existing appointment"
            )

    elif action == "decline":
        request_appointment.delete()
    else:
        raise WrongActionError("Action must be confirm or decline")
