from django.urls import path

from ..views import *


urlpatterns = [
    path("dashboard/", MentorDashboardPage.as_view()),
    path("mentees/", MentorMenteesPage.as_view()),
    path("mentees/<uuid:menteeid>/", MentorMenteePage.as_view()),
    path("mentees/<uuid:menteeid>/feedback/", MentorMenteePage.as_view()),
    path("mentees/<uuid:menteeid>/chat/", MentorMenteePage.as_view()),
    path("mentees/<uuid:menteeid>/plans/", MentorMenteePage.as_view()),
    path("mentees/<uuid:menteeid>/meetings/", MentorMenteePage.as_view()),
]
