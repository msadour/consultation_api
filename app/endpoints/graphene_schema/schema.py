import graphene
import graphene_django_optimizer as gql_optimizer
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug

from app.endpoints.booking.models import Appointment
from app.endpoints.surgeon.models import Surgeon


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment


class SurgeonType(DjangoObjectType):

    id = graphene.String()

    class Meta:
        model = Surgeon


class Query(graphene.ObjectType):
    all_appointments = graphene.List(AppointmentType)
    all_surgeons = graphene.List(SurgeonType)
    debug = graphene.Field(DjangoDebug, name="_debug")

    @staticmethod
    def resolve_all_appointments(root, info):
        return gql_optimizer.query(Appointment.objects.all(), info)

    @staticmethod
    def resolve_all_surgeons(root, info):
        return gql_optimizer.query(Surgeon.objects.all(), info)


schema = graphene.Schema(query=Query)
