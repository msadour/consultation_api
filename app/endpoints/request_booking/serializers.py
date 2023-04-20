from rest_framework import serializers

from app.endpoints.patient.models import Patient
from app.endpoints.request_booking.models import RequestAppointment
from app.endpoints.request_booking.utils import get_appointments_requested
from app.endpoints.surgeon.models import Surgeon


class AppointmentRequestSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        patient_id: str = validated_data.get("patient_id")
        patient: Patient = Patient.objects.get(id=patient_id)

        surgeon_id: str = validated_data.get("surgeon_id")
        surgeon: Surgeon = Surgeon.objects.get(id=surgeon_id)

        request_appointments = validated_data.get("request_appointments")
        appointments_available: list = get_appointments_requested(
            surgeon=surgeon,
            patient=patient,
            request_appointments=request_appointments,
        )
        RequestAppointment.objects.bulk_create(appointments_available)

    class Meta:
        model = RequestAppointment
        fields = "__all__"
