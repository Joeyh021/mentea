import uuid

from django.db import models


class User:
    # Main user model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    business_area = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserType:
    # Mentor or mentee
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)


class BusinessArea:
    # Business areas within the company
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_area = models.CharField(max_length=50)


class MentorMentee:
    # Mentor-mentee relationship
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentor", db_index=True
    )
    mentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentee", db_index=True
    )
    approved = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["mentee", "mentor"])]


class Notification:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Topic:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=50)


class UserTopic:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["user", "topic"])]


class Rating:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentor_rating", db_index=True
    )
    rating = models.IntegerField()
    associated_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    rated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rated_by",
        db_index=True,
        blank=True,
        null=True,
    )


class PlanOfAction:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    associated_mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plan_of_action_mentor",
        db_index=True,
    )
    associated_mentee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plan_of_action_mentee",
        db_index=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PlanOfActionTarget:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    achieved_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    associated_poa = models.ForeignKey(
        PlanOfAction, on_delete=models.CASCADE, db_index=True
    )
    set_by = models.ForeignKey(
        User, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_mentor", db_index=True
    )
    mentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_mentee", db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    content = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
