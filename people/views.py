from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistrationForm


from .forms import (
    PlanOfActionForm,
    ProfileForm,
    BusinessAreaForm,
    TopicForm,
    RegistrationForm,
    CreateMeetingForm,
    MenteeRescheduleForm,
)

from .models import *
from .util import get_mentor

from events.models import Event, MeetingRequest, FeedbackForm, Questions

from datetime import datetime


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

    template_name = "people/register.html"

    form_class: Any = RegistrationForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully! Please now complete your profile before continuing.",
            )
            login(
                request,
                authenticate(
                    username=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                ),
            )
            return redirect("profile_edit")
        return render(request, self.template_name, {"form": form})


class UserProfilePage(LoginRequiredMixin, TemplateView):
    """Shows a user's profile page and allows them to edit it"""

    template_name: str = "people/profile.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        mentee_topics = UserTopic.objects.filter(
            user=request.user, usertype=UserType.Mentee
        )
        mentor_topics = UserTopic.objects.filter(
            user=request.user, usertype=UserType.Mentor
        )

        return render(
            request,
            self.template_name,
            {
                "mentee_topics": mentee_topics,
                "mentor_topics": mentor_topics,
                "my_profile": True,
            },
        )


class ViewUserProfilePage(LoginRequiredMixin, TemplateView):
    template_name: str = "people/profile.html"

    def get(self, request: HttpRequest, userId=None) -> HttpResponse:

        user = get_object_or_404(User, id=userId)

        mentee_topics = UserTopic.objects.filter(user=user, usertype=UserType.Mentee)
        mentor_topics = UserTopic.objects.filter(user=user, usertype=UserType.Mentor)

        return render(
            request,
            self.template_name,
            {
                "user": user,
                "mentee_topics": mentee_topics,
                "mentor_topics": mentor_topics,
                "my_profile": False,
            },
        )


class UserProfileEditPage(LoginRequiredMixin, TemplateView):
    """Allows a user to edit their profile"""

    template_name: str = "people/profile_edit.html"
    form_class: Any = ProfileForm
    ba_form_class: Any = BusinessAreaForm
    topic_form_class: Any = TopicForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class(
            initial={
                "bio": request.user.bio,
                "business_area": request.user.business_area,
                "mentee_topics": UserTopic.objects.filter(
                    user=request.user, usertype=UserType.Mentee
                ).values_list("topic", flat=True),
                "mentor_topics": UserTopic.objects.filter(
                    user=request.user, usertype=UserType.Mentor
                ).values_list("topic", flat=True),
                "usertype": request.user.user_type,
            }
        )

        ba_form = self.ba_form_class()
        topic_form = self.topic_form_class()

        return render(
            request,
            self.template_name,
            {"form": form, "ba_form": ba_form, "topic_form": topic_form},
        )

    def post(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        print(request.POST)
        if "business_area_new" in request.POST:
            # Process business area form
            ba_form = self.ba_form_class(request.POST)
            if ba_form.is_valid():
                new_ba = BusinessArea(
                    business_area=ba_form.cleaned_data["business_area_new"]
                )
                new_ba.save()

                # Show a message saying "Business area created" and redirect to profile page
                messages.success(request, "Business area created")
                return redirect("profile_edit")
            else:
                messages.error(request, "Error creating business area")
                return render(
                    request,
                    self.template_name,
                    {
                        "form": self.form_class(),
                        "ba_form": ba_form,
                        "topic_form": self.topic_form_class(),
                    },
                )
        elif "topic_new" in request.POST:
            # Process topic form
            topic_form = self.topic_form_class(request.POST)
            if topic_form.is_valid():
                new_topic = Topic(topic=topic_form.cleaned_data["topic_new"])
                new_topic.save()

                # Show a message saying "Topic created" and redirect to profile page
                messages.success(request, "Topic created")
                return redirect("profile_edit")
            else:
                messages.error(request, "Error creating topic")
                return render(
                    request,
                    self.template_name,
                    {
                        "form": self.form_class(),
                        "ba_form": self.ba_form_class(),
                        "topic_form": topic_form,
                    },
                )
        else:
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
                selected_mentee_topics = form.cleaned_data.get("mentee_topics", None)

                # Create UserTopic models storing these
                UserTopic.objects.filter(user=current_user).delete()
                for topic in selected_mentee_topics:
                    user_topic = UserTopic(
                        user=request.user,
                        topic=topic,
                        usertype=UserType.Mentee,
                    )
                    user_topic.save()

                # Get selected topics
                selected_mentor_topics = form.cleaned_data.get("mentor_topics", None)

                # Create UserTopic models storing these
                for topic in selected_mentor_topics:
                    user_topic = UserTopic(
                        user=request.user,
                        topic=topic,
                        usertype=UserType.Mentor,
                    )
                    user_topic.save()

                # Show a message saying "Profile updated" and redirect to profile page
                messages.success(request, "Profile updated")
                return redirect("profile")

            else:
                print(form.cleaned_data)

                # Show error messages and go back to form page
                messages.error(request, "Error updating profile")
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "ba_form": self.ba_form_class(),
                        "topic_form": self.topic_form_class(),
                    },
                )


class UserCalendarPage(LoginRequiredMixin, TemplateView):
    """Shows a user's calendar with all their upcoming meetings and events"""

    template_name: str = "people/calendar.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class UserNotificationsPage(LoginRequiredMixin, TemplateView):
    """Shows all of a users notifcations"""

    template_name: str = "people/notifications.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        resp = render(request, self.template_name, {})
        resp[
            "Content-Security-Policy"
        ] = "frame-ancestors 'self' https://localhost:8000"
        return resp

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            notifId = request.POST["notifId"]

            notification = Notification.objects.get(id=notifId)
            notification.read = True
            notification.save()

        except:
            pass

        resp = render(request, self.template_name, {})
        resp[
            "Content-Security-Policy"
        ] = "frame-ancestors 'self' https://localhost:8000"
        return resp


class MenteeDashboardPage(IsUserMenteeMixin, TemplateView):
    """A mentee's home page"""

    template_name: str = "people/mentee_dashboard.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        # need to check if date is after today
        upcoming_meetings = MeetingRequest.objects.filter(
            mentee=request.user, mentee_approved=True, mentor_approved=True
        )

        return render(
            request,
            self.template_name,
            {"upcoming_meetings": upcoming_meetings},
        )


class MenteeFeedbackPage(IsUserMenteeMixin, TemplateView):
    """A page for a mentee to discuss feedback with their mentor"""

    template_name: str = "people/mentee_feedback.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MenteePlansPage(IsUserMenteeMixin, TemplateView):
    """A mentee's plans of action page"""

    template_name: str = "people/plans.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        user_plans = PlanOfAction.objects.all().filter(
            associated_mentee=request.user.id
        )

        return render(
            request,
            self.template_name,
            {
                "base": "mentee_base.html",
                "plans_list": self.__parse_plans(user_plans),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print(request.POST)
        if "completed" in request.POST:
            target = PlanOfActionTarget.objects.get(name=request.POST["completed"])
            target.achieved = True
            target.save()
        return HttpResponseRedirect("")

    def __parse_plans(self, plans):
        plans_list = []
        for p in plans:
            plan_targets = PlanOfActionTarget.objects.filter(associated_poa=p)
            plans_list.append(
                {
                    "name": p.name,
                    "targets": list(plan_targets),
                    "progress": str(p.progress),
                }
            )
        return plans_list


class MenteeNewPlanPage(IsUserMenteeMixin, TemplateView):
    """allows a mentee to create a new plan of action for themselves"""

    template_name: str = "people/new_plan.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = PlanOfActionForm()
        return render(
            request,
            self.template_name,
            {"form": form, "base": "mentee_base.html"},
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        current_user = request.user
        form = PlanOfActionForm(request.POST)
        print(request.POST)

        if form.is_valid():
            plan_name = form.cleaned_data["name"]
            plan = PlanOfAction.objects.create(
                name=plan_name,
                associated_mentee=current_user,
                associated_mentor=get_mentor(current_user),
            )

            for i in range(1, 6):
                target = form.cleaned_data[f"target_{i}"]
                description = form.cleaned_data[f"description_{i}"]
                if target != "":
                    PlanOfActionTarget.objects.create(
                        name=target,
                        description=description,
                        associated_poa=plan,
                        set_by=request.user,
                    )

            return HttpResponseRedirect("/mentee/plans")
        else:
            messages.error(request, "Error creating plan")
            return render(
                request,
                self.template_name,
                {
                    "form": PlanOfActionForm(),
                },
            )


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

    template_name: str = "people/plans.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        current_mentee = User.objects.get(id=kwargs["menteeid"])
        user_plans = PlanOfAction.objects.all().filter(associated_mentee=current_mentee)

        return render(
            request,
            self.template_name,
            {
                "base": "mentor_base.html",
                "plans_list": self.__parse_plans(user_plans),
                "mentee_name": f"{current_mentee.first_name} {current_mentee.last_name}",
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print(request.POST)
        if "completed" in request.POST:
            target = PlanOfActionTarget.objects.get(name=request.POST["completed"])
            target.achieved = True
            target.save()
        return HttpResponseRedirect("")

    def __parse_plans(self, plans):
        plans_list = []
        for p in plans:
            plan_targets = PlanOfActionTarget.objects.filter(associated_poa=p)
            plans_list.append(
                {
                    "name": p.name,
                    "targets": list(plan_targets),
                    "progress": str(p.progress),
                }
            )
        return plans_list


class MentorMenteeNewPlanPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to create a new plan of action for their mentee"""

    template_name: str = "people/new_plan.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = PlanOfActionForm()
        current_mentee = User.objects.get(id=kwargs["menteeid"])
        print(current_mentee)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "base": "mentor_base.html",
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        current_user = request.user
        form = PlanOfActionForm(request.POST)
        current_mentee = User.objects.get(id=kwargs["menteeid"])
        print(request.POST)

        if form.is_valid():
            plan_name = form.cleaned_data["name"]
            plan = PlanOfAction.objects.create(
                name=plan_name,
                associated_mentor=current_user,
                associated_mentee=current_mentee,
            )

            for i in range(1, 6):
                target = form.cleaned_data[f"target_{i}"]
                description = form.cleaned_data[f"description_{i}"]
                if target != "":
                    PlanOfActionTarget.objects.create(
                        name=target,
                        description=description,
                        associated_poa=plan,
                        set_by=request.user,
                    )

            return HttpResponseRedirect("..")
        else:
            messages.error(request, "Error creating plan")
            return render(
                request,
                self.template_name,
                {
                    "form": PlanOfActionForm(),
                },
            )


class MentorMenteeMeetingsPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to view and manage meetings and meeting history for a specific mentee"""

    template_name: str = "people/mentor_meetings.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class MeetingRequestPage(TemplateView):
    """A mentee should be able to request a meeting with their mentor."""

    template_name = "people/request.html"
    form_class: Any = CreateMeetingForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {})

    def post(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            # Get the current user object
            current_user = request.user

            # Get the event information from the form
            event_name = form.cleaned_data["name"]
            start_time = form.cleaned_data["start_time"]
            duration = form.cleaned_data["duration"]
            location = form.cleaned_data["location"]
            user = request.user
            mentor = get_mentor(user)

            # Create feedback form
            ff = FeedbackForm(
                name="Feedback for " + meeting.name,
                desc="Please fill out this form honestly! It can only be submitted once!",
                allowsMultipleSubmissions=False,
                allowsEditingSubmissions=False,
            )
            ff.save()

            q1 = Questions(
                name="General Feedback",
                form=ff,
                required=False,
                order=1,
                type="textarea",
                type_data="",
            )
            q1.save()

            meeting.feedback_form = ff
            meeting.save()

            # Add event to database:
            meeting = Event(
                name=event_name,
                startTime=start_time,
                duration=duration,
                location=location,
                mentor=mentor,
                feedback_form=ff,
            )
            meeting.save()

            # Add event request to database:
            meeting_request = MeetingRequest(
                event=meeting,
                mentee=current_user,
                mentor_approved=False,
                mentee_approved=True,
            )
            meeting_request.save()

            # Show a message saying "Meeting request sent" and redirect to ?
            messages.success(request, "Meeting request sent")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error sending meeting request")
            return render(request, self.template_name, {})


class MenteePastMeetingsPage(IsUserMenteeMixin, TemplateView):
    """Allows mentee to view past meetings and provide feedback for them"""

    template_name = "people/mentee_past.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        # check if date is before today
        past_meetings = MeetingRequest.objects.filter(
            mentee=request.user, mentee_approved=True, mentor_approved=True
        )

        return render(
            request,
            self.template_name,
            {"past_meetings": past_meetings},
        )


class MenteePendingMeetingsPage(IsUserMenteeMixin, TemplateView):
    """Allows mentee to view and approve pending meetings"""

    template_name = "people/mentee_pending.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        past_meetings = MeetingRequest.objects.filter(
            mentee=request.user, mentee_approved=False, mentor_approved=True
        )

        return render(
            request,
            self.template_name,
            {"past_meetings": past_meetings},
        )

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # change mentee_approved to True for the given meeting
        messages.success(
            request,
            "Meeting successfully approved",
        )
        return redirect("dashboard")


class MenteeRescheduleMeetingPage(IsUserMenteeMixin, TemplateView):
    """Allows mentee to reschedule a meeting"""

    template_name = "people/mentee_reschedule"
    form_class: Any = MenteeRescheduleForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})

    def post(self, request, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            # Get the event object for the current meeting
            meeting = Event.objects.get(id=eventId)

            # Update the time and location
            meeting.startTime = form.cleaned_data["start_time"]
            meeting.duration = form.cleaned_data["duration"]
            meeting.location = form.cleaned_data["location"]
            meeting.save()

            # Get the meeting request object for the event
            meeting_request = MeetingRequest.objects.get(event=eventId)

            # Update the approval (mentee approved mentor not approved)
            meeting_request.mentee_approved = True
            meeting_request.mentor_approved = False

            # Show a message saying "Meeting request updated" and redirect to dashboard
            messages.success(request, "Meeting request updated")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error updating meeting request")
            return render(request, self.template_name, {})


class MenteeEditMeetingPage(IsUserMenteeMixin, TemplateView):
    """Allows mentee to edit a meeting"""

    template_name = "people/mentee_edit_meeting"
    form_class: Any = CreateMeetingForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})

    def post(self, request, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            # Get the event object for the current meeting
            meeting = Event.objects.get(id=eventId)

            # Update the name, time and location
            meeting.name = form.cleaned_data["name"]
            meeting.startTime = form.cleaned_data["start_time"]
            meeting.duration = form.cleaned_data["duration"]
            meeting.location = form.cleaned_data["location"]

            # Get the meeting request object for the event
            meeting_request = MeetingRequest.objects.get(event=eventId)

            # Update the approval (mentee approved mentor not approved)
            meeting_request.mentee_approved = True
            meeting_request.mentor_approved = False

            # Show a message saying "Meeting request updated" and redirect to dashboard
            messages.success(request, "Meeting updated, request sent to mentor")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error updating meeting")
            return render(request, self.template_name, {})
