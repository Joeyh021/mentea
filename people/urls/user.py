from django.urls import include, path

from ..views import *
from people.views import UserSignupPage

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    # path("login/", UserLoginPage.as_view(), name="login"),
    path("register/", UserSignupPage.as_view(), name="register"),
    path("calendar/", UserCalendarPage.as_view(), name="calendar"),
    path("profile/", UserProfilePage.as_view(), name="profile"),
    path("profile/edit/", UserProfileEditPage.as_view(), name="profile_edit"),
    path("notifications/", UserNotificationsPage.as_view(), name="notifications"),
    path("<uuid:userId>/", ViewUserProfilePage.as_view(), name="userview_any"),
]
