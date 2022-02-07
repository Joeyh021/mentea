from django.urls import path

from ..views import *


urlpatterns = [
    path("dashboard", MenteeDashboardPage.as_view()),
    path("feedback", MenteeFeedbackPage.as_view()),
    path("plans", MenteePlansPage.as_view()),
    path("chat", MenteeChatPage.as_view()),
    path("meetings", MenteeMeetingsPage.as_view()),
]
