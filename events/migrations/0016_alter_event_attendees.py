# Generated by Django 4.0.2 on 2022-02-25 14:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0015_alter_event_attendees"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(
                related_name="eusers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
