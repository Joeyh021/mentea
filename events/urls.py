from django.urls import path

from .views import *

app_name = "events"

urlpatterns = [
    path("", EventsIndexPage.as_view(), name="index"),
]
