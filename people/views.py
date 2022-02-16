from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any


class UserLoginPage(TemplateView):
    """The user log in page, with your standard email/password form"""

    template_name: str = "people/login.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class UserSignupPage(TemplateView):
    """Lets a user sign up with email, password, and business area"""

    template_name = "registration/register.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class UserProfilePage(LoginRequiredMixin, TemplateView):
    """Shows a user's profile page and allows them to edit it"""

    template_name: str = "people/profile.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:

        return render(request, self.template_name, {})


class UserCalendarPage(TemplateView):
    """Shows a user's calendar with all their upcoming meetings and events"""

    template_name: str = "people/calendar.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class UserNotificationsPage(TemplateView):
    """Shows all of a users notifcations"""

    template_name: str = "people/notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeDashboardPage(TemplateView):
    """A mentee's home page"""

    template_name: str = "people/mentee_dashboard.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeFeedbackPage(TemplateView):
    """A page for a mentee to discuss feedback with their mentor"""

    template_name: str = "people/mentee_feedback.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteePlansPage(TemplateView):
    """A mentee's plans of action page"""

    template_name: str = "people/mentee_plans.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeChatPage(TemplateView):
    """Chat between a mentee and their mentor"""

    template_name: str = "people/mentee_chat.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeMeetingsPage(TemplateView):
    """Upcoming meetings and records of past meetings between a mentee and their mentor"""

    template_name: str = "people/mentee_meetings.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorDashboardPage(TemplateView):
    """A mentor's home/dashboard page"""

    template_name: str = "people/mentor_dashboard.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteesPage(TemplateView):
    """A mentor's view of all his current mentess, along with new mentee requests"""

    template_name: str = "people/mentor_mentees.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


# possible rename due to ambiguous names
class MentorMenteePage(TemplateView):
    """A mentor's overview of a specfic mentee and their relationship"""

    template_name: str = "people/mentor_mentee.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteeFeedbackPage(TemplateView):
    """Feedback between the mentor and specific mentee"""

    template_name: str = "people/mentor_feedback.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteeChatPage(TemplateView):
    """Allows a mentor to send and view chats to a specific mentee"""

    template_name: str = "people/mentor_chat.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteePlansPage(TemplateView):
    """Allows a mentor to view and manage plans of action for a specific mentee"""

    template_name: str = "people/mentor_plans.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteeMeetingsPage(TemplateView):
    """Allows a mentor to view and manage meetings and meeting history for a specific mentee"""

    template_name: str = "people/mentor_meetings.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})
