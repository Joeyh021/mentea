# Generated by Django 4.0.2 on 2022-02-24 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0012_event_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="endTime",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
