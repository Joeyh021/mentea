# Generated by Django 4.0.2 on 2022-03-08 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0021_remove_eventrequest_events_even_request_beb3ea_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.CharField(
                choices=[("Workshops", "Workshop"), ("OneToOne", "One to One")],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="eventrequest",
            name="type",
            field=models.CharField(
                choices=[("Workshops", "Workshop"), ("OneToOne", "One to One")],
                max_length=50,
            ),
        ),
        migrations.DeleteModel(
            name="EventType",
        ),
    ]