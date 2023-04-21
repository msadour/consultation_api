from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.patient.models import Patient
from app.endpoints.request_booking.models import RequestAppointment
from app.endpoints.request_booking.serializers import AppointmentRequestSerializer
from app.endpoints.request_booking.utils import retrieve_future_requests
from app.endpoints.surgeon.models import Surgeon
from app.layer.permissions import (
    RequestSurgeonUpdatePermission,
    IsPatientPermission,
    IsSurgeonPermission,
)


class PatientAppointmentRequestViewSet(viewsets.ViewSet):

    serializer_class = AppointmentRequestSerializer
    queryset = RequestAppointment.objects.all().order_by("-date")
    permission_classes = [
        IsAuthenticated,
        IsPatientPermission,
    ]

    def create(self, request: Request) -> Response:
        data: dict = request.data.copy()
        data["patient_id"] = request.user.id
        self.serializer_class().create(validated_data=data)
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request: Request) -> Response:
        patient: Patient = Patient.objects.filter(user_id=request.user.id).first()
        all_requests: QuerySet = self.queryset.filter(patient=patient)
        data: dict = self.serializer_class(all_requests, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class SurgeonAppointmentRequestViewSet(viewsets.ViewSet):

    serializer_class = AppointmentRequestSerializer
    model = RequestAppointment
    permission_classes = [
        IsAuthenticated,
        IsSurgeonPermission,
        RequestSurgeonUpdatePermission,
    ]

    def list(self, request: Request) -> Response:
        surgeon: Surgeon = Surgeon.objects.filter(user_id=request.user.id).first()
        future_requests: QuerySet = retrieve_future_requests(surgeon=surgeon).order_by(
            "-date"
        )
        data: dict = self.serializer_class(future_requests, many=True).data
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
