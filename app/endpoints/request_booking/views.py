from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.patient.models import Patient
from app.endpoints.request_booking.models import RequestAppointment
from app.endpoints.request_booking.serializers import AppointmentRequestSerializer
from app.endpoints.surgeon.models import Surgeon


class PatientAppointmentRequestViewSet(viewsets.ViewSet):

    serializer_class = AppointmentRequestSerializer
    model = RequestAppointment

    def create(self, request: Request) -> Response:
        data: dict = request.data.copy()
        data["patient_id"] = request.user.id
        self.serializer_class().create(validated_data=data)
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request: Request) -> Response:
        patient = Patient.objects.filter(user_id=request.user.id).first()
        all_requests = RequestAppointment.objects.filter(patient=patient)
        data = self.serializer_class(all_requests, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class SurgeonAppointmentRequestViewSet(viewsets.ViewSet):

    serializer_class = AppointmentRequestSerializer
    model = RequestAppointment

    def list(self, request: Request) -> Response:
        surgeon: Surgeon = Surgeon.objects.filter(user_id=request.user.id).first()
        all_requests: RequestAppointment = RequestAppointment.objects.filter(
            surgeon=surgeon
        )
        data: dict = self.serializer_class(all_requests, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        request_appointment_id: str = request.data.get("request_appointment_id")
        request_appointment: RequestAppointment = RequestAppointment.objects.get(
            id=request_appointment_id
        )
        self.serializer_class().update(
            instance=request_appointment, validated_data=request.data
        )
        return Response(status=status.HTTP_200_OK)
