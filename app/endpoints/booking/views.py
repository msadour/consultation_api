from django.db.models.query import QuerySet
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.booking.models import Appointment
from app.endpoints.booking.serializers import AppointmentSerializer
from app.endpoints.patient.models import Patient
from app.endpoints.surgeon.models import Surgeon


class AppointmentManagementPatientViewSet(viewsets.ViewSet):

    serializer_class = AppointmentSerializer
    model = Appointment

    def list(self, request: Request) -> Response:
        patient: Patient = Patient.objects.filter(user_id=request.user.id).first()
        all_appointments: QuerySet = self.model.objects.filter(patient=patient)
        data: dict = self.serializer_class(all_appointments, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None) -> Response:
        appointment: QuerySet = self.model.objects.get(id=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentManagementSurgeonViewSet(viewsets.ViewSet):

    serializer_class = AppointmentSerializer
    model = Appointment

    def list(self, request: Request) -> Response:
        surgeon: Surgeon = Surgeon.objects.filter(user_id=request.user.id).first()
        all_appointments: QuerySet = self.model.objects.filter(surgeon=surgeon)
        data: dict = self.serializer_class(all_appointments, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
