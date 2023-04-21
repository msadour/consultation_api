from rest_framework import serializers

from app.endpoints.booking.models import Appointment, Status
from app.endpoints.patient.serializers import PatientSerializer
from app.endpoints.surgeon.serializers import SurgeonSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    surgeon = SurgeonSerializer()
    patient = PatientSerializer()

    def update(self, instance, validated_data):
        action: str = validated_data.get("action", "cancel")
        if action == "cancel":
            instance.status = Status.CANCEL

        instance.save()

    class Meta:
        model = Appointment
        fields = "__all__"
