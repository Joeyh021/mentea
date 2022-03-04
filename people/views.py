from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegistrationForm, SendMessageForm


from .forms import (
    PlanOfActionForm,
    ProfileForm,
    BusinessAreaForm,
    TopicForm,
    RegistrationForm,
)
from .models import *
from .util import get_mentor


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
        return render(request, self.template_name, {})


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

        if "menteeid" in kwargs:
            current_mentee = User.objects.get(id=kwargs["menteeid"])
            templateBase = "mentor_base.html"
        else:
            current_mentee = request.user
            templateBase = "mentee_base.html"

        current_mentor = get_mentor(current_mentee)
        form = SendMessageForm()
        chatMessages = ChatMessage.objects.all().filter(
            chat=Chat.objects.get(mentee=current_mentee, mentor=current_mentor)
        )

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
                "form": form,
                "base": templateBase,
                "chatMessages": chatMessages,
                "mentee": current_mentee,
                "mentor": current_mentor,
            },
        )


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
