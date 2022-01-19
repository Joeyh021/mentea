from django.urls import path

from .views import *

app_name = "relationships"

urlpatterns = [
    path("", RelationshipsIndexPage.as_view(), name="index"),
]
