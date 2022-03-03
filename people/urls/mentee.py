from django.urls import path

from ..views import *


urlpatterns = [
    path("", MenteeDashboardPage.as_view(), name="dashboard"),
    path("feedback/", MenteeFeedbackPage.as_view(), name="feedback"),
    path("plans", MenteePlansPage.as_view(), name="plans"),
    path("plans/new", MenteeNewPlanPage.as_view(), name="new_plan"),
    path("chat/", ChatPage.as_view(), name="chat"),
    path("meetings/", MenteeMeetingsPage.as_view(), name="meetings"),
]
