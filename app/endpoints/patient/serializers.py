from rest_framework import serializers

from app.endpoints.patient.models import Patient
from app.layer.common.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"
