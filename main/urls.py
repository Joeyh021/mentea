from django.urls import path

from .views import *

app_name = "main"

urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("faq", FAQPage.as_view()),
    path("privacy", PrivacyPage.as_view()),
    path("feedback", FeedbackPage.as_view()),
]
