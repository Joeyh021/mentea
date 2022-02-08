from django.urls import path

from .views import *

app_name = "events"

# see views.py for a description of each URL
urlpatterns = [
    path("", EventsIndexPage.as_view(), name="index"),
    path("create/", EventCreatePage.as_view()),
    path("request/", EventRequestPage.as_view()),
    path("<uuid:eventid>/", EventPage.as_view()),
]
