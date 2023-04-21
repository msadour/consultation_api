from datetime import datetime, time, timedelta

from django.db.models import Q
from django.db.models.query import QuerySet

from app.endpoints.booking.models import Appointment
from app.endpoints.booking.models import Status as AppointmentStatus
from app.endpoints.patient.models import Patient
from app.endpoints.request_booking.models import RequestAppointment, Status
from app.endpoints.surgeon.models import Surgeon
from app.layer.exception import WrongActionError, WrongTimeError


def _add_delta(tme: datetime.time, delta: timedelta, operand: str) -> datetime.time:
    if operand == "-":
        return (datetime.combine(datetime.today(), tme) - delta).time()
    else:
        return (datetime.combine(datetime.today(), tme) + delta).time()


def is_too_late(date_appointment: datetime, begin_at: time) -> bool:
    date_appointment_over: bool = (
        date_appointment.timestamp() < datetime.today().timestamp()
    )
    if date_appointment_over:
        return True
    elif date_appointment.timestamp() == datetime.today().timestamp():
        time_appointment_minus_1h: time = _add_delta(
            begin_at, timedelta(hours=1), operand="-"
        )
        time_appointment_over: bool = (
            time_appointment_minus_1h <= datetime.today().time()
        )
        if time_appointment_over:
            return True

    return False


def check_10_minutes_around_appointment(
    appointments_surgeon: QuerySet, begin_at: datetime, finish_at: datetime
):
    finish_at_plus_10m: datetime.time = finish_at + timedelta(minutes=10)
    begin_at_minus_10m: datetime.time = begin_at - timedelta(minutes=10)
    query_10_minutes_around_appointment: bool = appointments_surgeon.filter(
        Q(date__gte=finish_at_plus_10m) | Q(finish_at__lte=begin_at_minus_10m)
    ).exists()
    return not query_10_minutes_around_appointment


def get_appointments_requested(
    surgeon: Surgeon, patient: Patient, request_appointments: list
):
    appointments_requested: list = []

    appointment: dict
    for appointment in request_appointments:
        date_str: str = appointment["date"]
        date: datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        begin_at: time = date.time()

        if (
            not is_too_late(date_appointment=date, begin_at=begin_at)
            or time(9, 00) > begin_at
            or begin_at > time(14, 15)
            or date.weekday() > 4
        ):
            continue

        finish_at: datetime = date + timedelta(minutes=45)
        appointment.update({"finish_at": finish_at, surgeon: surgeon, patient: patient})
        appointments_requested.append(appointment)

    return [
        RequestAppointment(
            surgeon=surgeon,
            patient=patient,
            date=appointment_available.get("date"),
            finish_at=appointment_available.get("finish_at"),
        )
        for appointment_available in appointments_requested
    ]


def update_appointment_request(request_appointment: RequestAppointment, action: str):
    if action == "confirm":
        date: datetime = request_appointment.date
        begin_at: time = date.time()
        finish_at: datetime = request_appointment.finish_at
        surgeon: Surgeon = request_appointment.surgeon
        patient: Patient = request_appointment.patient

        if is_too_late(date_appointment=date, begin_at=begin_at):
            raise WrongTimeError(
                "You cannot accept an appointment which is before today or less than 1 hour from now"
            )

        appointments_surgeon: QuerySet = Appointment.objects.filter(
            surgeon=surgeon
        ).filter(status=AppointmentStatus.BOOKED)

        is_appointment_already_exist: bool = appointments_surgeon.filter(
            date=date
        ).exists()

        if (
            is_appointment_already_exist is False
            and check_10_minutes_around_appointment(
                appointments_surgeon=appointments_surgeon,
                begin_at=date,
                finish_at=finish_at,
            )
        ):
            Appointment.objects.create(
                surgeon=surgeon,
                patient=patient,
                date=date,
                finish_at=finish_at,
            )
            request_appointment.status = Status.ACCEPTED
            request_appointment.save()
        else:
            raise WrongTimeError(
                "You cannot have multiple appointment on the same day, or around 10 minutes of an existing appointment"
            )

    elif action == "decline":
        request_appointment.delete()
    else:
        raise WrongActionError("Action must be confirm or decline")


def retrieve_future_requests(surgeon: Surgeon) -> QuerySet:
    current_date: datetime = datetime.now()
    future_requests: QuerySet = (
        RequestAppointment.objects.filter(surgeon=surgeon)
        .filter(date__gte=current_date)
        .filter(status=Status.PENDING)
    )
    return future_requests
