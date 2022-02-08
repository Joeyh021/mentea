from django.urls import path

from ..views import *


urlpatterns = [
    path("login/", UserLoginPage.as_view(),name="login"),
    path("register/", UserSignupPage.as_view(),name="register"),
    path("calendar/", UserCalendarPage.as_view(),name="calendar"),
    path("profile/", UserProfilePage.as_view(),name="profile"),
    path("notifications/", UserNotificationsPage.as_view(),name="notifications"),
]
