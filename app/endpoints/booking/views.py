from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.booking.serializers import AppointmentSerializer


class AppointmentManagementPatientViewSet(viewsets.ViewSet):

    serializer_class = AppointmentSerializer

    def list(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentManagementSurgeonViewSet(viewsets.ViewSet):

    serializer_class = AppointmentSerializer

    def list(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)
