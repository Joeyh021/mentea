from django.contrib import admin
import django_stubs_ext

from people.models import BusinessArea, User, UserType

django_stubs_ext.monkeypatch()

from events.models import (
    Answer,
    DefaultFeedbackForms,
    FeedbackForm,
    FeedbackSubmission,
    Questions,
)

# Register your models here.


@admin.register(FeedbackForm)
class AdminFeedbackForm(admin.ModelAdmin[FeedbackForm]):
    list_display = ("name",)
    pass


@admin.register(FeedbackSubmission)
class AdminFeedbackSubmission(admin.ModelAdmin[FeedbackSubmission]):
    pass


@admin.register(Questions)
class AdminQuestion(admin.ModelAdmin[Questions]):
    pass


@admin.register(Answer)
class AdminAnswer(admin.ModelAdmin[Answer]):
    pass


@admin.register(DefaultFeedbackForms)
class AdminDefaultFeedbackForms(admin.ModelAdmin[DefaultFeedbackForms]):
    pass
