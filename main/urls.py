from django.urls import path

from .views import *

app_name = "main"

urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("faq/", FAQPage.as_view(), name="faq"),
    path("privacy/", PrivacyPage.as_view(), name="privacy"),
    path("feedback/", FeedbackPage.as_view(), name="feedback"),
    path("terms-of-service/", TermosOfServicePage.as_view(), name="tos"),
]
