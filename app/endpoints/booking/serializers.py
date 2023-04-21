from rest_framework import serializers

from app.endpoints.booking.models import Appointment, Status


class AppointmentSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        action: str = validated_data.get("action", "cancel")
        if action == "cancel":
            instance.status = Status.CANCEL

        instance.save()

    class Meta:
        model = Appointment
        fields = "__all__"
