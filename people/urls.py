from django.urls import path

from .views import *

app_name = "people"

urlpatterns = [
    path("", PeopleIndexView.as_view(), name="index"),
]
