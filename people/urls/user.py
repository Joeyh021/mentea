from django.urls import path

from ..views import *


urlpatterns = [
    path("login", UserLoginPage.as_view()),
    path("register", UserSignupPage.as_view()),
    path("calendar", UserCalendarPage.as_view()),
    path("profile", UserProfilePage.as_view()),
    path("notifications", UserNotificationsPage.as_view()),
]
