from typing import Any

from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.booking.models import Appointment
from app.endpoints.booking.serializers import AppointmentSerializer
from app.endpoints.booking.utils import retrieve_future_appointments
from app.endpoints.patient.models import Patient
from app.endpoints.surgeon.models import Surgeon
from app.layer.permissions import (
    AppointmentUpdatePermission,
    IsPatientPermission,
    IsSurgeonPermission,
)


class AppointmentManagementBaseViewSet(viewsets.ViewSet):
    serializer_class: AppointmentSerializer = AppointmentSerializer
    model: Appointment = Appointment
    user_model: Any = None
    queryset: QuerySet = Appointment.objects.all().order_by("-date")
    permission_classes: tuple = ()

    def list(self, request: Request) -> Response:
        current_user: Any = self.user_model.objects.filter(
            user_id=request.user.id
        ).first()
        all_appointments: QuerySet = retrieve_future_appointments(
            current_user=current_user, user_model=self.user_model
        )
        data: dict = self.serializer_class(all_appointments, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        appointment_id: str = request.data.get("appointment_id")
        appointment: Appointment = self.model.objects.get(id=appointment_id)
        self.serializer_class().update(
            instance=appointment, validated_data=request.data
        )
        return Response(status=status.HTTP_200_OK)


class AppointmentManagementPatientViewSet(AppointmentManagementBaseViewSet):

    user_model: Patient = Patient
    permission_classes: tuple = (
        IsAuthenticated,
        IsPatientPermission,
        AppointmentUpdatePermission,
    )


class AppointmentManagementSurgeonViewSet(AppointmentManagementBaseViewSet):

    user_model: Surgeon = Surgeon
    permission_classes: tuple = (
        IsAuthenticated,
        IsSurgeonPermission,
    )
