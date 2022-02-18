from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any

from .forms import ProfileForm
from .models import UserTopic


class IsUserMenteeMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.user_type == "Mentee"
            or self.request.user.user_type == "MentorMentee"
        )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IsUserMentorMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.user_type == "Mentor"
            or self.request.user.user_type == "MentorMentee"
        )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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


class UserProfileEditPage(LoginRequiredMixin, TemplateView):
    """Allows a user to edit their profile"""

    template_name: str = "people/profile_edit.html"
    form_class: Any = ProfileForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class(
            initial={
                "bio": request.user.bio,
                "business_area": request.user.business_area,
                "topics": UserTopic.objects.filter(user=request.user).values_list(
                    "topic", flat=True
                ),
                "usertype": request.user.user_type,
            }
        )
        current_user = request.user

        # Currently we only allow users to pick from business areas or topics that exist. We need to add the option to add missing ones.

        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            # Get the current user object
            current_user = request.user

            # Add bio and business area to it and save
            current_user.bio = form.cleaned_data["bio"]
            current_user.business_area = form.cleaned_data["business_area"]
            current_user.user_type = form.cleaned_data["usertype"]
            current_user.save()

            # Get selected topics
            selected_topics = form.cleaned_data.get("topics", None)

            # Create UserTopic models storing these
            UserTopic.objects.filter(user=current_user).delete()
            for topic in selected_topics:
                user_topic = UserTopic(
                    user=request.user,
                    topic=topic,
                    usertype=form.cleaned_data["usertype"],
                )
                user_topic.save()

            # Show a message saying "Profile updated" and redirect to profile page
            messages.success(request, "Profile updated")
            return redirect("profile")

        else:
            print(form.cleaned_data)

            # Show error messages and go back to form page
            messages.error(request, "Error updating profile")
            return render(request, self.template_name, {"form": form})


class UserCalendarPage(LoginRequiredMixin, TemplateView):
    """Shows a user's calendar with all their upcoming meetings and events"""

    template_name: str = "people/calendar.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class UserNotificationsPage(LoginRequiredMixin, TemplateView):
    """Shows all of a users notifcations"""

    template_name: str = "people/notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeDashboardPage(IsUserMenteeMixin, TemplateView):
    """A mentee's home page"""

    template_name: str = "people/mentee_dashboard.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeFeedbackPage(IsUserMenteeMixin, TemplateView):
    """A page for a mentee to discuss feedback with their mentor"""

    template_name: str = "people/mentee_feedback.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteePlansPage(IsUserMenteeMixin, TemplateView):
    """A mentee's plans of action page"""

    template_name: str = "people/mentee_plans.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeChatPage(IsUserMenteeMixin, TemplateView):
    """Chat between a mentee and their mentor"""

    template_name: str = "people/mentee_chat.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteeMeetingsPage(IsUserMenteeMixin, TemplateView):
    """Upcoming meetings and records of past meetings between a mentee and their mentor"""

    template_name: str = "people/mentee_meetings.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorDashboardPage(IsUserMentorMixin, TemplateView):
    """A mentor's home/dashboard page"""

    template_name: str = "people/mentor_dashboard.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteesPage(IsUserMentorMixin, TemplateView):
    """A mentor's view of all his current mentess, along with new mentee requests"""

    template_name: str = "people/mentor_mentees.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


# possible rename due to ambiguous names
class MentorMenteePage(IsUserMentorMixin, TemplateView):
    """A mentor's overview of a specfic mentee and their relationship"""

    template_name: str = "people/mentor_mentee.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteeFeedbackPage(IsUserMentorMixin, TemplateView):
    """Feedback between the mentor and specific mentee"""

    template_name: str = "people/mentor_feedback.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteeChatPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to send and view chats to a specific mentee"""

    template_name: str = "people/mentor_chat.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteePlansPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to view and manage plans of action for a specific mentee"""

    template_name: str = "people/mentor_plans.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MentorMenteeMeetingsPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to view and manage meetings and meeting history for a specific mentee"""

    template_name: str = "people/mentor_meetings.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})
