import uuid

from django.db import models


class Event:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    startTime = models.DateTimeField()
    duration = models.IntegerField()
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE)


class EventType:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    max_members = models.IntegerField()
    min_members = models.IntegerField()


class EventAttendee:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)


class FeedbackForm:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
