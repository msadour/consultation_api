from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from app.endpoints.patient.models import Patient
from app.endpoints.patient.serializers import PatientSerializer
from app.layer.permissions import PatientPermission


class PatientProfileViewSet(viewsets.GenericViewSet):

    serializer_class: PatientSerializer = PatientSerializer
    permission_classes: tuple = (IsAuthenticated, PatientPermission)

    def retrieve(self, request: Request, pk=None) -> Response:
        patient: Patient = Patient.objects.filter(id=pk).first()
        data: dict = self.serializer_class(patient).data
        return Response(data=data, status=status.HTTP_200_OK)
