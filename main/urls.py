from django.urls import path

from .views import *

app_name = "main"

urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
]
