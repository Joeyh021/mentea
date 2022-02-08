from django.urls import path

from ..views import *


urlpatterns = [
    path("dashboard/", MentorDashboardPage.as_view(), name="dashboard"),
    path("mentees/", MentorMenteesPage.as_view(), name="mentees"),
    path("mentees/<uuid:menteeid>/", MentorMenteePage.as_view(), name="mentee"),
    path(
        "mentees/<uuid:menteeid>/feedback/", MentorMenteePage.as_view(), name="feedback"
    ),
    path("mentees/<uuid:menteeid>/chat/", MentorMenteePage.as_view(), name="chat"),
    path("mentees/<uuid:menteeid>/plans/", MentorMenteePage.as_view(), name="plans"),
    path(
        "mentees/<uuid:menteeid>/meetings/", MentorMenteePage.as_view(), name="meetings"
    ),
]
