from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from app.endpoints.surgeon.models import Surgeon
from app.endpoints.surgeon.serializers import SurgeonSerializer


class SurgeonAvailableViewSet(viewsets.ViewSet):

    queryset: QuerySet = Surgeon.objects.all().cache()
    serializer_class: SurgeonSerializer = SurgeonSerializer

    def list(self, request: Request) -> Response:
        data: dict = self.serializer_class(self.queryset, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
