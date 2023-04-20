from datetime import datetime, timedelta, time

from app.endpoints.patient.models import Patient
from app.endpoints.request_booking.models import RequestAppointment
from app.endpoints.surgeon.models import Surgeon


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
