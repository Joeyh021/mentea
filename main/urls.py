"""URLS for app main. Also includes URLs for the feedback form API"""
from django.urls import path


from .views import *

from .feedback import *

app_name = "main"


urlpatterns = [
    path("", IndexPage.as_view(), name="index"),  # home page
    path("faq/", FAQPage.as_view(), name="faq"),  # FAQ page
    path("privacy/", PrivacyPage.as_view(), name="privacy"),  # privacy information
    path(
        "feedback/", FeedbackPage.as_view(), name="feedback"
    ),  # application feedback form
    path(
        "terms-of-service/", TermosOfServicePage.as_view(), name="tos"
    ),  # terms of service information
    path(
        "feedback-api/<uuid:formId>/",
        FeedbackFormReturn.as_view(),
        name="ff-get",
    ),
    path(
        "feedback-api/create/",
        FeedbackFormCreate.as_view(),
        name="ff-create",
    ),
    path(
        "feedback-api/editor-edit/",
        FeedbackFormEditorEdit.as_view(),
        name="ff-editor-edit",
    ),
    path(
        "feedback-api/submission/",
        FeedbackFormSubmissionHandler.as_view(),
        name="ff-submission",
    ),
    path(
        "feedback-api/submission/<uuid:submissionId>",
        FeedbackFormSubmissionHandler.as_view(),
        name="ff-submission",
    ),
    path(
        "feedback-api/submission-update/",
        FeedbackFormSubmissionUpdateHandler.as_view(),
        name="ff-submission",
    ),
    path("feedback-api/builder/", FeedbackFormBuilder.as_view(), name="ff-builder"),
    path(
        "feedback-api/<uuid:formId>/submissions/",
        FeedbackFormSubmissions.as_view(),
        name="ff-submissions",
    ),
]
