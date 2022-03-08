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
        "mentee_edit_meeting/<uuid:eventId>",
        MenteeEditMeetingPage.as_view(),
        name="mentee_edit_meeting",
    ),
    path("view_notes/", MenteeViewMeetingNotesPage.as_view(), name="view_notes"),
    path("add_notes/", MenteeAddMeetingNotesPage.as_view(), name="add_notes"),
    path("edit_notes/", MenteeEditMeetingNotesPage.as_view(), name="edit_notes"),
]
