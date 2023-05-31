from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.surgeon.models import Surgeon
from app.endpoints.surgeon.serializers import SurgeonSerializer
from app.endpoints.surgeon.tasks.task import create_surgeon_task


class SurgeonAvailableViewSet(viewsets.ViewSet):

    queryset: QuerySet = Surgeon.objects.all()
    serializer_class: SurgeonSerializer = SurgeonSerializer

    def list(self, request: Request) -> Response:
        data: dict = self.serializer_class(self.queryset, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class SurgeonTaskViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        create_surgeon_task()
        return Response(data={"message": "task created"}, status=status.HTTP_200_OK)
