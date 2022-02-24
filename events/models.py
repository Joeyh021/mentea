from datetime import datetime, timedelta
from random import randint
from django.utils import timezone
import uuid

from django.db import models
from people.models import *


class FeedbackForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    acceptingSubmissionsUntil = models.DateTimeField(blank=True, null=True)
    allowsMultipleSubmissions = models.BooleanField(default=True)
    allowsEditingSubmissions = models.BooleanField(default=False)


class FeedbackSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Questions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    type_data = models.JSONField()
    form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE)
    order = models.IntegerField()
    required = models.BooleanField()


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    associated_question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    associated_submission = models.ForeignKey(
        FeedbackSubmission, on_delete=models.CASCADE
    )
    data = models.CharField(max_length=200)


class DefaultFeedbackForms(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    feedback = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE)

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()  # Since only one item

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)


class EventType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    max_members = models.IntegerField()
    min_members = models.IntegerField()


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.TextField()
    duration = models.IntegerField()
    description = models.TextField(blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE, null=True, default=None)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, default=None)
    
    def calc_end_date(self):
        return self.startTime + timedelta(minutes=self.duration)
    
    def has_event_finished(self):
        return self.calc_end_date() < timezone.now()
    
    def get_pattern(self):
        return 'bg-pattern-' + str(randint(1,3))
    
    def in_progress(self):
        return self.startTime < timezone.now() and self.endTime > timezone.now()
    
    


class EventAttendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["event", "attendee"])]


class EventRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    associated_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
