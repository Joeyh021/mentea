# Generated by Django 4.0.2 on 2022-03-10 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0012_mentormentee_created_at_mentormentee_updated_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rating",
            name="associated_topic",
        ),
    ]