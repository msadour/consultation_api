from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Marks the specified blog post as published."

    def handle(self, *args, **options):
        call_command("loaddata", "./fixtures/data.json")
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
