import uuid

from django.db import models


class Document:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to="documents/")
    associated_user = models.ForeignKey( # Probably better as a polymorphi type
        "User", on_delete=models.CASCADE, blank=True, null=True
    )
    associated_event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AppFeedback:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feedback = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
