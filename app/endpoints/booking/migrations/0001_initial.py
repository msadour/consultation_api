# Generated by Django 4.2 on 2023-04-20 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("surgeon", "0001_initial"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("finish_at", models.DateTimeField()),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patient.patient",
                    ),
                ),
                (
                    "surgeon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="surgeon.surgeon",
                    ),
                ),
            ],
        ),
    ]
