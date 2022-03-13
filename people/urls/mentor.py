from django.urls import path

from ..views import *


urlpatterns = [
    path("", MentorDashboardPage.as_view(), name="mentor_dashboard"),
    path("mentees/<uuid:menteeId>/", MentorMenteePage.as_view(), name="mentee"),
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
        "mentees/<uuid:menteeId>/end-mentorship/",
        EndMentorshipMentor.as_view(),
        name="end_mentorship_mentor",
    ),
    path(
        "mentor_upcoming/", MentorUpcomingMeetingsPage.as_view(), name="mentor_upcoming"
    ),
    path("mentor_past/", MentorPastMeetingsPage.as_view(), name="mentor_past"),
    path("mentor_pending/", MentorPendingMeetingsPage.as_view(), name="mentor_pending"),
    path(
        "mentor_reschedule/<uuid:eventId>/",
        MentorRescheduleMeetingPage.as_view(),
        name="mentor_reschedule",
    ),
    path(
        "meeting/<uuid:meetingId>/",
        ViewMeetingPage.as_view(),
        name="mentor_view_meeting",
    ),
    path(
        "meeting/<uuid:meetingId>/notes/",
        MentorViewMeetingNotesPage.as_view(),
        name="mentor_view_notes",
    ),
    path(
        "meeting/<uuid:meetingId>/notes/add/",
        MentorAddMeetingNotesPage.as_view(),
        name="mentor_add_notes",
    ),
    path(
        "meeting/<uuid:meetingId>/notes/<uuid:noteId>/",
        MentorEditMeetingNotesPage.as_view(),
        name="mentor_edit_notes",
    ),
    path(
        "meeting/<uuid:meetingId>/feedback/",
        MentorMeetingFeedbackPage.as_view(),
        name="mentor_meeting_feedback",
    ),
    path(
        "mentees/<uuid:menteeId>/give_general_feedback/",
        MentorGiveGeneralFeedbackPage.as_view(),
        name="mentor_give_general_feedback",
    ),
    path(
        "view_general_feedback/",
        MentorViewGeneralFeedbackPage.as_view(),
        name="mentor_view_general_feedback",
    ),
]
