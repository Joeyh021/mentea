from django.urls import path

from .views import *

app_name = "events"

# see views.py for a description of each URL
urlpatterns = [
    path("", EventsIndexPage.as_view(), name="workshop-index"),
    path("previous/", EventsPreviousPage.as_view(), name="workshop-prev"),
    path("create/", EventCreatePage.as_view(), name="workshop-create"),
    path("<uuid:eventId>/edit", EventEditPage.as_view(), name="workshop-edit"),
    path("request/", EventRequestPage.as_view(), name="workshop-request"),
    path("<uuid:eventId>/", EventPage.as_view(), name="workshop"),
    path(
        "<uuid:eventId>/toggleAttendance",
        EventToggleAttendance.as_view(),
        name="workshop-toggleattendance",
    ),
    path(
        "<uuid:eventId>/delete",
        EventDelete.as_view(),
        name="workshop-delete",
    ),
]
