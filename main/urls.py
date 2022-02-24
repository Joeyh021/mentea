

from django.urls import path




from .views import *

from .feedback import *

app_name = "main"





urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("faq/", FAQPage.as_view(), name="faq"),
    path("privacy/", PrivacyPage.as_view(), name="privacy"),
    path("feedback/", FeedbackPage.as_view(), name="feedback"),
    path("terms-of-service/", TermosOfServicePage.as_view(), name="tos"),
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
]
