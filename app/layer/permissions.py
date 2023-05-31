from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from app.endpoints.booking.models import Appointment
from app.endpoints.request_booking.models import RequestAppointment


class AppointmentUpdatePermission(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: ViewSet, obj: Appointment
    ) -> bool:
        return (
            request.user.id == obj.patient.user_id
            or request.user.id == obj.surgeon.user_id
        )


class RequestSurgeonUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            request_appointment_id: str = request.data.get("request_appointment_id")
            return RequestAppointment.objects.filter(
                id=request_appointment_id, surgeon__user_id=request.user.id
            ).exists()

        return True


class PatientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.kwargs.get("pk") == str(request.user.id)


class IsPatientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "patient_user")


class IsSurgeonPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "surgeon_user")
