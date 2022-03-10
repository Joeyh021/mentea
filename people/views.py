from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.contrib.auth import login, authenticate
from django.contrib import messages


from events.notification import NotificationManager

from .forms import RegistrationForm, SendMessageForm


from .forms import (
    PlanOfActionForm,
    ProfileForm,
    BusinessAreaForm,
    TopicForm,
    RegistrationForm,
    CreateMeetingForm,
    MenteeRescheduleForm,
    MentorRescheduleForm,
    CreateMeetingNotesForm,
)

from .models import *
from .util import get_mentor, mentor_mentors_mentee

from events.models import (
    Event,
    EventRequest,
    EventType,
    MeetingRequest,
    FeedbackForm,
    Questions,
    MeetingNotes,
)

from datetime import datetime, timedelta

from django.db.models import Q


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


class MenteeHasMentorMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            get_mentor(self.request.user)
            return True
        except:
            return False

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
        upcoming_meetings_ids = MeetingRequest.objects.filter(
            mentee=request.user,
            mentee_approved=True,
            mentor_approved=True,
        ).all()

        upcoming_meetings = Event.objects.filter(
            id__in=upcoming_meetings_ids, endTime__gte=datetime.now()
        ).all()

        mm = MentorMentee.objects.filter(mentee=request.user).select_related("mentor")

        return render(
            request,
            self.template_name,
            {"upcoming_meetings": upcoming_meetings, "mm": mm},
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


class ChatPage(LoginRequiredMixin, TemplateView):
    """Chat between a mentee and their mentor"""

    template_name: str = "people/chat.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        current_mentor = None

        if "menteeid" in kwargs:
            current_mentee = User.objects.get(id=kwargs["menteeid"])
            current_mentor = request.user
            templateBase = "mentor_base.html"
        else:
            current_mentee = request.user
            templateBase = "mentee_base.html"
            try:
                current_mentor = get_mentor(current_mentee)
            except:
                return HttpResponse("no mentor")

        form = SendMessageForm()

        chat = None
        try:
            chat = Chat.objects.get(mentee=current_mentee, mentor=current_mentor)
        except:
            chat = Chat(mentee=current_mentee, mentor=current_mentor)
            chat.save()

        chatMessages = ChatMessage.objects.all().filter(chat=chat)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "base": templateBase,
                "chatMessages": chatMessages,
                "mentee": current_mentee,
                "mentor": current_mentor,
            },
        )

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        if "menteeid" in kwargs:
            current_mentee = User.objects.get(id=kwargs["menteeid"])
            templateBase = "mentor_base.html"
        else:
            current_mentee = request.user
            templateBase = "mentee_base.html"

        current_mentor = get_mentor(current_mentee)
        form = SendMessageForm(request.POST)
        print(request.POST)

        if form.is_valid():
            text = form.cleaned_data["content"]
            ChatMessage.objects.create(
                chat=Chat.objects.get(mentee=current_mentee, mentor=current_mentor),
                content=text,
                sender=request.user,
            )
        else:
            messages.error(request, "Error sending a message")

        chatMessages = ChatMessage.objects.all().filter(
            chat=Chat.objects.get(mentee=current_mentee, mentor=current_mentor)
        )
        return render(
            request,
            self.template_name,
            {
                "form": SendMessageForm(),
                "base": templateBase,
                "chatMessages": chatMessages,
                "mentee": current_mentee,
                "mentor": current_mentor,
            },
        )


class ChatMessages(LoginRequiredMixin, TemplateView):

    template_name: str = "people/chat_messages.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        current_mentor = None

        if "menteeid" in kwargs:
            current_mentee = User.objects.get(id=kwargs["menteeid"])
            current_mentor = request.user
            templateBase = "mentor_base.html"
        else:
            current_mentee = request.user
            templateBase = "mentee_base.html"
            try:
                current_mentor = get_mentor(current_mentee)
            except:
                return HttpResponse("no mentor")

        form = SendMessageForm()

        chat = None
        try:
            chat = Chat.objects.get(mentee=current_mentee, mentor=current_mentor)
        except:
            chat = Chat(mentee=current_mentee, mentor=current_mentor)
            chat.save()

        chatMessages = ChatMessage.objects.all().filter(chat=chat)

        resp = render(
            request,
            self.template_name,
            {
                "base": templateBase,
                "chatMessages": chatMessages,
                "mentee": current_mentee,
                "mentor": current_mentor,
            },
        )
        resp[
            "Content-Security-Policy"
        ] = "frame-ancestors 'self' https://localhost:8000"

        return resp


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

    template_name: str = "mentor_mentee/relationship.html"

    def get(self, request: HttpRequest, menteeId=None) -> HttpResponse:

        mentee = get_object_or_404(User, id=menteeId)

        hasRelation, relation = mentor_mentors_mentee(request.user, mentee)

        if not hasRelation:
            return render(request, "mentor_mentee/no_relationship.html", {})
        else:
            return render(
                request,
                self.template_name,
                {
                    "mentor": relation.mentor,
                    "mentee": relation.mentee,
                    "relation": relation,
                },
            )


class MentorMenteeFeedbackPage(IsUserMentorMixin, TemplateView):
    """Feedback between the mentor and specific mentee"""

    template_name: str = "people/mentor_feedback.html"

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

            mentor = target.associated_poa.associated_mentor
            mentee = target.associated_poa.associated_mentee

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
                    "id": p.id,
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
            NotificationManager.send(
                "New Plan of Action",
                current_user.get_full_name()
                + " has created a new Plan of Action for you!",
                current_mentee,
                "/mentee/plans/",
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
        form.updateQSToUser(request.user)
        return render(request, self.template_name, {"form": form})

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
            mentor = form.cleaned_data["mentor"]

            # Create feedback form
            ff = FeedbackForm(
                name="Feedback for " + event_name,
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

            etype = EventType.objects.get(name="121")

            endTime = start_time + timedelta(minutes=duration)
            # Add event to database:
            meeting = Event(
                name=event_name,
                startTime=start_time,
                endTime=endTime,
                duration=duration,
                location=location,
                mentor=mentor,
                feedback_form=ff,
                type=etype,
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

            NotificationManager.send(
                "1-2-1 Meeting Request",
                current_user.get_full_name()
                + ", has requested a 1-2-1 meeting with you!",
                mentor,
                "",
            )

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
        past_meetings_id = MeetingRequest.objects.filter(
            mentee=request.user,
            mentee_approved=True,
            mentor_approved=True,
        ).all()

        past_meetings = Event.objects.filter(
            id__in=past_meetings_id, endTime__lt=datetime.now()
        ).all()

        return render(
            request,
            self.template_name,
            {"past_meetings": past_meetings},
        )


class MenteePendingMeetingsPage(IsUserMenteeMixin, TemplateView):
    """Allows mentee to view and approve pending meetings"""

    template_name = "people/mentee_pending.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        pending_meetings = MeetingRequest.objects.filter(
            Q(mentee_approved = False) | Q(mentor_approved = False),
            mentee=request.user,
            )

        return render(
            request,
            self.template_name,
            {"pending_meetings": pending_meetings},
        )

    def post(self, request, eventId=None) -> HttpResponse:
        # Get the current meeting object
        current_meeting = MeetingRequest.objects.get(id=eventId)
        # update the mentee_approved field
        current_meeting.mentee_approved = True
        messages.success(
            request,
            "Meeting successfully approved",
        )
        return redirect("dashboard")


class MenteeRescheduleMeetingPage(IsUserMenteeMixin, TemplateView):
    """Allows mentee to reschedule a meeting"""

    template_name = "people/mentee_reschedule.html"
    form_class: Any = MenteeRescheduleForm

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:

        event = get_object_or_404(Event, id=eventId)

        form = self.form_class(
            initial={
                "start_time": event.startTime.replace(tzinfo=None).isoformat(),
                "duration": event.duration,
                "location": event.location,
            }
        )

        return render(request, self.template_name, {"form": form})

    def post(self, request, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            # Get the event object for the current meeting
            meeting = Event.objects.get(id=eventId)

            endTime = form.cleaned_data["start_time"] + timedelta(
                minutes=form.cleaned_data["duration"]
            )

            # Update the time and location
            meeting.startTime = form.cleaned_data["start_time"]
            meeting.duration = form.cleaned_data["duration"]
            meeting.location = form.cleaned_data["location"]
            meeting.endTime = endTime
            meeting.save()

            # Get the meeting request object for the event
            meeting_request = MeetingRequest.objects.get(event=eventId)

            # Update the approval (mentee approved mentor not approved)
            meeting_request.mentee_approved = True
            meeting_request.mentor_approved = False

            meeting_request.save()

            NotificationManager.send(
                "1-2-1 Meeting Reschedule",
                request.user.get_full_name()
                + ", has rescheduled a 1-2-1 meeting with you! Please re-confirm it",
                meeting.mentor,
                "",
            )

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

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:
        meeting = get_object_or_404(Event, id=eventId)

        form = self.form_class(
            initial={
                "name": meeting.name,
                "start-time": meeting.startTime,
                "duration": meeting.duration,
                "location": meeting.location,
            }
        )
        return render(request, self.template_name, {"form":form})

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

class MenteeUpcomingMeetingsPage(IsUserMenteeMixin, TemplateView):
    """Allows a mentee to view upcoming meetings and access their editing and rescheduling pages"""

    template_name = "people/mentee_upcoming.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        upcoming_meetings_id = MeetingRequest.objects.filter(
            mentee=request.user,
            mentee_approved=True,
            mentor_approved=True,
        ).all()

        upcoming_meetings = Event.objects.filter(
            id__in=upcoming_meetings_id, endTime__gte=datetime.now()
        ).all()

        mm = MentorMentee.objects.filter(mentee=request.user).select_related("mentor")

        return render(
            request,
            self.template_name,
            {"upcoming_meetings": upcoming_meetings, "mm": mm},
        )




class MentorUpcomingMeetingsPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to view their upcoming meetings"""

    template_name = "people/mentor_upcoming.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        # could also filter for each mentee in particular

        upcoming_meetings_id = MeetingRequest.objects.filter(
            mentee_approved=True,
            mentor_approved=True,
        ).all()

        upcoming_meetings = Event.objects.filter(
            id__in=upcoming_meetings_id, endTime__gte=datetime.now(), mentor=request.user
        ).all()

        return render(
            request,
            self.template_name,
            {"upcoming_meetings": upcoming_meetings},
        )


class MentorPastMeetingsPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to view their previous meetings"""

    template_name = "people/mentor_past.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        # could also filter for each mentee in particular

        past_meetings_id = MeetingRequest.objects.filter(
            mentee_approved=True,
            mentor_approved=True,
        ).all()

        past_meetings = Event.objects.filter(
            mentor=request.user,
            endTime__lt=datetime.now(),
        ).all()

        return render(
            request,
            self.template_name,
            {"past_meetings": past_meetings},
        )


class MentorPendingMeetingsPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to view meetings they haven't approved yet"""

    template_name = "people/mentor_pending.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        pending_meetings = MeetingRequest.objects.filter(
            Q(mentee_approved = False) | Q(mentor_approved = False),
            mentee=request.user,
            )

        return render(
            request,
            self.template_name,
            {"pending_meetings": pending_meetings},
        )

    def post(self, request, eventId=None) -> HttpResponse:
        # Get the current meeting object
        current_meeting = MeetingRequest.objects.get(id=eventId)
        # update the mentor_approved field
        current_meeting.mentor_approved = True
        messages.success(
            request,
            "Meeting successfully approved",
        )
        return redirect("dashboard")

class MentorRescheduleMeetingPage(IsUserMentorMixin, TemplateView):
    """Allows mentor to reschedule a meeting"""

    template_name = "people/mentor_reschedule"
    form_class: Any = MentorRescheduleForm

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:

        event = get_object_or_404(Event, id=eventId)

        form = self.form_class(
            initial={
                "start_time": event.startTime.replace(tzinfo=None).isoformat(),
                "duration": event.duration,
                "location": event.location,
            }
        )

        return render(request, self.template_name, {"form": form})

    def post(self, request, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            # Get the event object for the current meeting
            meeting = Event.objects.get(id=eventId)

            endTime = form.cleaned_data["start_time"] + timedelta(
                minutes=form.cleaned_data["duration"]
            )

            # Update the time and location
            meeting.startTime = form.cleaned_data["start_time"]
            meeting.duration = form.cleaned_data["duration"]
            meeting.location = form.cleaned_data["location"]
            meeting.endTime = endTime
            meeting.save()

            # Get the meeting request object for the event
            meeting_request = MeetingRequest.objects.get(event=eventId)

            # Update the approval (mentoe approved mentee not approved)
            meeting_request.mentee_approved = False
            meeting_request.mentor_approved = True

            meeting_request.save()

            NotificationManager.send(
                "1-2-1 Meeting Reschedule",
                request.user.get_full_name()
                + ", has rescheduled a 1-2-1 meeting with you! Please re-confirm it",
                meeting.mentee,
                "",
            )

            # Show a message saying "Meeting request updated" and redirect to dashboard
            messages.success(request, "Meeting request updated")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error updating meeting request")
            return render(request, self.template_name, {})


class MentorEditMeetingPage(IsUserMentorMixin, TemplateView):
    """Allows mentor to edit a meeting"""

    template_name = "people/mentor_edit_meeting"
    form_class: Any = CreateMeetingForm

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:
        meeting = get_object_or_404(Event, id=eventId)

        form = self.form_class(
            initial={
                "name": meeting.name,
                "start-time": meeting.startTime,
                "duration": meeting.duration,
                "location": meeting.location,
            }
        )
        return render(request, self.template_name, {"form":form})

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

            # Update the approval (mentor approved mentee not approved)
            meeting_request.mentee_approved = False
            meeting_request.mentor_approved = True

            # Show a message saying "Meeting request updated" and redirect to dashboard
            messages.success(request, "Meeting updated, request sent to mentor")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error updating meeting")
            return render(request, self.template_name, {})

class MenteeViewMeetingNotesPage(IsUserMenteeMixin, TemplateView):
    """Allows the mentee to view the notes for a past meeting"""

    template_name = "people/mentee_view_notes.html"

    def get(self, request, eventId=None) -> HttpResponse:

        meeting_notes = MeetingNotes.objects.get(id=eventId).all()

        return render(
            request,
            self.template_name,
            {"meeting_notes": meeting_notes},
        )



class MenteeAddMeetingNotesPage(IsUserMenteeMixin, TemplateView):
    """Allows a mentee to add meeting notes"""

    template_name = "people/mentee_add_notes.html"

    form_class: Any = CreateMeetingNotesForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            mentee = request.user
            mentor = get_mentor(mentee)
            meeting = Event.objects.get(id=eventId)
            content = form.cleaned_data["content"]

            note = MeetingNotes(
                event=meeting, mentee=mentee, mentor=mentor, content=content
            )

            note.save()

            # Show a message saying "Meeting note saved" and redirect to ?
            messages.success(request, "Meeting note saved")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error saving meeting note")
            return render(request, self.template_name, {})


class MenteeEditMeetingNotesPage(IsUserMenteeMixin, TemplateView):
    """Allows the mentee to edit a meeting note"""

    template_name = "people/mentee_edit_notes.html"
    form_class: Any = CreateMeetingNotesForm

    def get(self, request: HttpRequest, noteId=None) -> HttpResponse:
        note = get_object_or_404(MeetingNotes, id=noteId)

        form = self.form_class(
            initial={
                "content": note.content,
            }
        )
        return render(request, self.template_name, {"form":form})

    def post(self, request, noteId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            # get note
            note = MeetingNotes.objects.get(id=noteId)
            # edit the note
            note.content = form.cleaned_data["content"]

            messages.success(request, "Meeting note succesfully updated")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error updating meeting note")
            return render(request, self.template_name, {})


class MentorViewMeetingNotesPage(IsUserMentorMixin, TemplateView):
    """Allows the mentor to view the notes for a past meeting"""

    template_name = "people/mentoe_view_notes.html"

    def get(self, request, eventId=None) -> HttpResponse:

        meeting_notes = MeetingNotes.objects.get(id=eventId).all()

        return render(
            request,
            self.template_name,
            {"meeting_notes": meeting_notes},
        )


class MentorAddMeetingNotesPage(IsUserMentorMixin, TemplateView):
    """Allows a mentor to add meeting notes"""

    template_name = "people/mentor_add_notes.html"

    form_class: Any = CreateMeetingNotesForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {})

    def post(self, request, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():

            mentor = request.user
            # not sure how to get the mentee here
            mentee = mentor
            meeting = Event.objects.get(id=eventId)
            content = form.cleaned_data["content"]

            note = MeetingNotes(
                event=meeting, mentee=mentee, mentor=mentor, content=content
            )

            note.save()

            # Show a message saying "Meeting note saved" and redirect to ?
            messages.success(request, "Meeting note saved")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error saving meeting note")
            return render(request, self.template_name, {})


class MentorEditMeetingNotesPage(IsUserMentorMixin, TemplateView):
    """Allows the mentor to edit a meeting note"""

    template_name = "people/mentor_edit_notes.html"
    form_class: Any = CreateMeetingNotesForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})

    def post(self, request, noteId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            # get note
            note = MeetingNotes.objects.get(id=noteId)
            # edit the note
            note.content = form.cleaned_data["content"]

            messages.success(request, "Meeting note succesfully updated")
            return redirect("dashboard")

        else:

            # Show error messages and go back to ?
            messages.error(request, "Error updating meeting note")
            return render(request, self.template_name, {})
