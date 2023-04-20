from rest_framework import serializers

from app.endpoints.surgeon.models import Surgeon
from app.layer.common.serializers import UserSerializer


class SurgeonSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Surgeon
        fields = "__all__"
