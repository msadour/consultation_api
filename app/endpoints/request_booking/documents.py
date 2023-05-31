from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import RequestAppointment


@registry.register_document
class RequestAppointmentDocument(Document):
    class Index:

        name = "cars"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = RequestAppointment

        fields = [
            "date",
            "finish_at",
            "status",
        ]
