from django.urls import path

from ..views import *


urlpatterns = [
    path("", MentorDashboardPage.as_view(), name="mentor_dashboard"),
    path("mentees/", MentorMenteesPage.as_view(), name="mentees"),
    path("mentees/<uuid:menteeId>/", MentorMenteePage.as_view(), name="mentee"),
    path(
        "mentees/<uuid:menteeid>/feedback/",
        MentorMenteeFeedbackPage.as_view(),
        name="feedback",
    ),
    path("mentees/<uuid:menteeid>/chat/", ChatPage.as_view(), name="chat"),
    path("mentees/<uuid:menteeid>/chat/messages/", ChatMessages.as_view(), name="chat"),
    path(
        "mentees/<uuid:menteeid>/plans/",
        MentorMenteePlansPage.as_view(),
        name="mentor_plans",
    ),
    path(
        "mentees/<uuid:menteeid>/plans/new/",
        MentorMenteeNewPlanPage.as_view(),
        name="new_mentor_plan",
    ),
    path(
        "mentees/<uuid:menteeid>/meetings/",
        MentorMenteeMeetingsPage.as_view(),
        name="meetings",
    ),
    path(
        "mentor_upcoming/", MentorUpcomingMeetingsPage.as_view(), name="mentor_upcoming"
    ),
    path("mentor_past/", MentorPastMeetingsPage.as_view(), name="mentor_past"),
    path("mentor_pending/", MentorPendingMeetingsPage.as_view(), name="mentor_pending"),
    path(
        "mentor_reschedule/<uuid:eventId>",
        MentorRescheduleMeetingPage.as_view(),
        name="mentor_reschedule",
    ),
    path(
        "mentor_edit_meeting/<uuid:eventId>",
        MentorEditMeetingPage.as_view(),
        name="mentor_edit_meeting",
    ),
    path("view_notes/", MentorViewMeetingNotesPage.as_view(), name="view_notes"),
    path("add_notes/", MentorAddMeetingNotesPage.as_view(), name="add_notes"),
    path("edit_notes/", MentorEditMeetingNotesPage.as_view(), name="edit_notes"),
]
