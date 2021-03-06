from datetime import timedelta
from django.utils import timezone

from people.models import *


class EventType(models.TextChoices):
    Workshop = "Workshops"
    OneToOne = "OneToOne", "One to One"


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


class GeneralFeedbackForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submitted_by"
    )
    submitted_for = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submitted_for"
    )
    feedback = models.TextField(blank=True)


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.TextField()
    duration = models.IntegerField()
    description = models.TextField(blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=EventType.choices)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_form = models.ForeignKey(
        FeedbackForm, on_delete=models.CASCADE, null=True, default=None
    )
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, default=None)
    attendees = models.ManyToManyField(User, related_name="eusers")

    def calc_end_date(self):
        return self.startTime + timedelta(minutes=self.duration)

    def has_event_finished(self):

        return self.calc_end_date() < timezone.now()

    def get_pattern(self):
        numb = 0
        for d in str(self.id):
            if d.isdigit():
                numb = int(d)
                break

        return "bg-pattern-" + str((numb % 3) + 1)

    def in_progress(self):
        return self.startTime < timezone.now() and self.endTime > timezone.now()

    def has_finished(self):
        return self.endTime < timezone.now()

    def current_user_is_part_of_event(self, user: User):
        # Check if they are the mentor
        if self.current_user_is_mentor(user):
            return True
        try:
            u = self.attendees.get(id=user.id)
            return True
        except:
            return False

    def current_user_is_mentor(self, user: User):
        return self.mentor == user

    def get_mentee(self):
        return self.attendees.first()


class EventAttendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["event", "attendee"])]


class EventRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=EventType.choices)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    associated_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["requested_by", "associated_topic"], name="unique_request"
            )
        ]


class MeetingRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    mentor_approved = models.BooleanField()
    mentee_approved = models.BooleanField()


class MeetingNotes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    content = models.CharField(max_length=500)
