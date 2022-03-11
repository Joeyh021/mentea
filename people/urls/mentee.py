from django.urls import path

from ..views import *


urlpatterns = [
    path("", MenteeDashboardPage.as_view(), name="dashboard"),
    path("feedback/", MenteeFeedbackPage.as_view(), name="feedback"),
    path("plans/", MenteePlansPage.as_view(), name="plans"),
    path("plans/new/", MenteeNewPlanPage.as_view(), name="new_plan"),
    path("chat/", ChatPage.as_view(), name="chat"),
    path("chat/messages/", ChatMessages.as_view(), name="chat"),
    path("meetings/", MenteeMeetingsPage.as_view(), name="meetings"),
    path("mentee_past/", MenteePastMeetingsPage.as_view(), name="mentee_past"),
    path("mentee_pending/", MenteePendingMeetingsPage.as_view(), name="mentee_pending"),
    path(
        "mentee_reschedule/<uuid:eventId>",
        MenteeRescheduleMeetingPage.as_view(),
        name="mentee_reschedule",
    ),
    path("request/", MeetingRequestPage.as_view(), name="request"),
    path(
        "mentee_upcoming/", MenteeUpcomingMeetingsPage.as_view(), name="mentee_upcoming"
    ),
    path(
        "meeting/<uuid:meetingId>/notes/",
        MenteeViewMeetingNotesPage.as_view(),
        name="view_notes",
    ),
    path(
        "meeting/<uuid:meetingId>/notes/add/",
        MenteeAddMeetingNotesPage.as_view(),
        name="add_notes",
    ),
    path(
        "meeting/<uuid:meetingId>/notes/<uuid:noteId>/",
        MenteeEditMeetingNotesPage.as_view(),
        name="edit_notes",
    ),
    path(
        "meeting/<uuid:meetingId>/feedback/",
        MenteeMeetingFeedbackPage.as_view(),
        name="meeting_feedback",
    ),
    path(
        "give_general_feedback/",
        MenteeGiveGeneralFeedbackPage.as_view(),
        name="give_general_feedback",
    ),
    path(
        "view_general_feedback/",
        MenteeViewGeneralFeedbackPage.as_view(),
        name="view_general_feedback",
    ),
    path("meeting/<uuid:meetingId>/", ViewMeetingPage.as_view(), name="view_meeting"),
    path("choose-mentor/", ChooseMentorPage.as_view(), name="choose_mentor"),
    
    path("end-mentorship/", EndMentorship.as_view(), name="end_mentorship")
]
