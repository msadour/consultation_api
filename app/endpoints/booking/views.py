from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.booking.models import Appointment
from app.endpoints.booking.serializers import AppointmentSerializer
from app.endpoints.patient.models import Patient
from app.endpoints.surgeon.models import Surgeon
from app.layer.permissions import (
    AppointmentPatientDestroyPermission,
    IsPatientPermission,
    IsSurgeonPermission,
)


class AppointmentManagementPatientViewSet(viewsets.ViewSet):

    serializer_class: AppointmentSerializer = AppointmentSerializer
    model: Appointment = Appointment
    queryset: QuerySet = Appointment.objects.all().order_by("-date")
    permission_classes: tuple = (
        IsAuthenticated,
        IsPatientPermission,
        AppointmentPatientDestroyPermission,
    )

    def list(self, request: Request) -> Response:
        patient: Patient = Patient.objects.filter(user_id=request.user.id).first()
        all_appointments: QuerySet = self.queryset.filter(patient=patient)
        data: dict = self.serializer_class(all_appointments, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: str = None) -> Response:
        appointment: QuerySet = self.model.objects.get(id=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentManagementSurgeonViewSet(viewsets.ViewSet):

    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all().order_by("-date")
    permission_classes = [
        IsAuthenticated,
        IsSurgeonPermission,
    ]

    def list(self, request: Request) -> Response:
        surgeon: Surgeon = Surgeon.objects.filter(user_id=request.user.id).first()
        all_appointments: QuerySet = self.queryset.filter(surgeon=surgeon)
        data: dict = self.serializer_class(all_appointments, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
