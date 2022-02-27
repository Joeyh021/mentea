from django.urls import path

from ..views import *


urlpatterns = [
    path("", MentorDashboardPage.as_view(), name="mentor_dashboard"),
    path("mentees/", MentorMenteesPage.as_view(), name="mentees"),
    path("mentees/<uuid:menteeid>/", MentorMenteePage.as_view(), name="mentee"),
    path(
        "mentees/<uuid:menteeid>/feedback/",
        MentorMenteeFeedbackPage.as_view(),
        name="feedback",
    ),
    path("mentees/<uuid:menteeid>/chat/", MentorMenteeChatPage.as_view(), name="chat"),
    path(
        "mentees/<uuid:menteeid>/plans/", MentorMenteePlansPage.as_view(), name="plans"
    ),
    path(
        "mentees/<uuid:menteeid>/meetings/",
        MentorMenteeMeetingsPage.as_view(),
        name="meetings",
    ),
]
