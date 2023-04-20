from rest_framework import permissions
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from app.endpoints.booking.models import Appointment
from app.endpoints.request_booking.models import RequestAppointment


class AppointmentPatientDestroyPermission(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: ViewSet, obj: Appointment
    ) -> bool:
        return request.user.id == obj.patient.user_id


class RequestSurgeonUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            request_appointment_id: str = request.data.get("request_appointment_id")
            request_appointment: RequestAppointment = RequestAppointment.objects.get(
                id=request_appointment_id
            )
            return request_appointment.surgeon.user_id == request.user.id

        return True