from datetime import datetime, timedelta, timezone
import json
from typing_extensions import Required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from events.forms import WorkshopForm, WorkshopRequestForm
from people.models import Notification, Topic, UserTopic

from .models import (
    Event,
    EventAttendee,
    EventRequest,
    EventType,
    FeedbackForm,
    Questions,
)

from django.core.paginator import Paginator
from django.db.models import F, Count, Q


class EventsIndexPage(LoginRequiredMixin, TemplateView):
    """
    The main workshops page, containing a list of all currently scheduled workshops and links to their individual pages.
    Should also contain UI to link to /create (if authenticated as mentor), and to /request (if authenticated as mentee)
    """

    template_name = "workshops/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:

        my_events = (
            request.user.eusers.order_by("startTime")
            .filter(endTime__gte=datetime.now())
            .all()
        )
        my_running_events = Event.objects.filter(
            mentor=request.user, endTime__gte=datetime.now()
        )

        # return HttpResponse(my_events)

        event_list = (
            Event.objects.order_by("startTime")
            .filter(endTime__gte=datetime.now())
            .all()
        )
        paginator = Paginator(event_list, 9)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        requested = False
        try:
            request.GET["requested"]
            requested = True
        except:
            pass

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "my_events": my_events.union(my_running_events),
                "requested": requested,
            },
        )


class EventsPreviousPage(LoginRequiredMixin, TemplateView):
    """
    The main workshops page, containing a list of all currently scheduled workshops and links to their individual pages.
    Should also contain UI to link to /create (if authenticated as mentor), and to /request (if authenticated as mentee)
    """

    template_name = "workshops/previous.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:

        my_events = (
            request.user.eusers.order_by("startTime")
            .filter(endTime__lte=datetime.now())
            .all()
        )
        my_running_events = Event.objects.order_by("startTime").filter(
            mentor=request.user, endTime__lte=datetime.now()
        )

        # return HttpResponse(my_events)

        paginator = Paginator(my_events.union(my_running_events), 9)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {"page_obj": page_obj})


class EventRequestPage(TemplateView):
    """
    Mentees should be able to express interest in a new workshop around a specific topic here.
    """

    template_name = "workshops/request.html"
    form_class: Any = WorkshopRequestForm

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        
  
        
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Get current user (a mentor)

            formData = form.cleaned_data

            etype = EventType.objects.get(name="WORKSHOP")

            eventRequest = EventRequest(
                requested_by=request.user,
                type=etype,
                associated_topic=formData["topic"],
            )
            try:
                eventRequest.save()
            except:
                pass  # We don't care if the unique constraint fails, as far as the user is aware they have requested a session

            # Check if multiple requests for the same topic exist, if so suggest to mentors that they run an event
            dups = (
                EventRequest.objects.values("associated_topic")
                .annotate(count=Count("associated_topic"))
                .values("associated_topic")
                .order_by()
                .filter(count__gte=2)
            )

            interested = Topic.objects.filter(
                id__in=dups
            )  # Contains a list of topics with atleast 3 requests

            for topic in interested:
                # First gather all mentors that are interested in mentoring the topic, and then send them a notification

                mentors = UserTopic.objects.filter(
                    Q(usertype="Mentor") | Q(usertype="MentorMentee"), topic=topic
                )
                for m in mentors:
                    mentor = m.user
                    notif = Notification(
                        user=mentor,
                        title="Event Request",
                        content="Multiple mentees are interested in a topic area you teach: "
                        + topic.topic,
                        link = "/workshops/create?topic=" + str(topic.id)
                    )
                    notif.save()

                # return HttpResponse(mentors)

            return redirect("/workshops/?requested")

        else:
            messages.error(request, "Error creating workshop!")
            return render(request, self.template_name, {"form": form})


class EventCreatePage(TemplateView):
    """
    Mentors should be able to see what topics are frequently requested and schedule new workshops here.
    """

    template_name = "workshops/create.html"

    form_class: Any = WorkshopForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class()
        
        try:
            id = request.GET['topic']
            form = self.form_class(initial={
                "topic": id
            })
            form.fields['topic'].widget.attrs['style'] = "background-color: rgba(0,0,0,0.2); pointer-events: none"
        except:
            pass
        
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            # Get current user (a mentor)

            formData = form.cleaned_data

            etype = EventType.objects.get(name="WORKSHOP")

            startTime = formData["startTime"]
            endTime = startTime + timedelta(minutes=formData["duration"])

            event = Event(
                name=formData["name"],
                startTime=formData["startTime"],
                endTime=endTime,
                duration=formData["duration"],
                location="Online",
                mentor=request.user,
                type=etype,
                description=formData["desc"],
                topic=formData["topic"],
            )
            event.save()

            # Build form here
            ff = FeedbackForm(
                name="Feedback for " + event.name,
                desc="Please fill out this form honestly! It can only be submitted once!",
                allowsMultipleSubmissions=False,
                allowsEditingSubmissions=False,
            )
            ff.save()

            q_data = json.loads(
                '{"options": [{"key": "Yes", "value": "dc9ba51f-d768-48f4-905f-a8a458a459b9"}, {"key": "No", "value": "278f8734-69f7-48ae-8a9b-f5efc9fa9f17"}]}'
            )

            q1 = Questions(
                name="Did you enjoy the workshop?",
                form=ff,
                type="select",
                required=True,
                order=0,
                type_data=q_data,
            )
            q1.save()

            q2 = Questions(
                name="General Feedback",
                form=ff,
                required=False,
                order=1,
                type="textarea",
                type_data="",
            )
            q2.save()

            event.feedback_form = ff
            event.save()
            
            # Clear all event requests for this topic, and notify the users
            
            topic = Topic.objects.get(topic=formData['topic'])
            eventReq = EventRequest.objects.filter(associated_topic=topic)
            for er in eventReq:
                notif = Notification(
                        user=er.requested_by,
                        title="Event Available",
                        content="A workshop on " + topic.topic + " that you requested is now available!",
                        link = "/workshops/" + str(event.id)
                    )
                notif.save()
                er.delete()

            return redirect("/workshops/" + str(event.id) + "/")

        else:
            messages.error(request, "Error creating workshop!")
            return render(request, self.template_name, {"form": form})


class EventEditPage(TemplateView):
    """
    Mentors should be able to see what topics are frequently requested and schedule new workshops here.
    """

    template_name = "workshops/edit.html"

    form_class: Any = WorkshopForm

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:

        event = get_object_or_404(Event, id=eventId)

        form = self.form_class(
            initial={
                "name": event.name,
                "startTime": event.startTime.replace(tzinfo=None).isoformat(),
                "duration": event.duration,
                "topic": event.topic,
                "desc": event.description,
            }
        )
        return render(request, self.template_name, {"form": form, "eId": eventId})

    def post(self, request: HttpRequest, eventId=None) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            # Get current user (a mentor)

            formData = form.cleaned_data

            startTime = formData["startTime"]
            endTime = startTime + timedelta(minutes=formData["duration"])

            event = get_object_or_404(Event, id=eventId)
            event.name = formData["name"]
            event.duration = formData["duration"]
            event.startTime = startTime
            event.endTime = endTime
            event.description = formData["desc"]
            event.save()

            # Build form here

            return redirect("/workshops/" + str(event.id) + "/?edited")

        else:
            messages.error(request, "Error creating workshop!")
            return render(request, self.template_name, {"form": form})


class EventPage(TemplateView):
    """
    A page for each event, containing info about the event, whos running it, attendees, and anything else.
    """

    # not sure what best practice is for this template name
    template_name = "workshops/event.html"

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:

        event = Event.objects.get(id=eventId)

        userHasJoined = event.current_user_is_part_of_event(request.user)

        edited = False
        try:
            request.GET["edited"]
            edited = True
        except:
            pass

        return render(
            request,
            self.template_name,
            {
                "event": event,
                "registeredToEvent": userHasJoined,
                "isMentor": event.current_user_is_mentor(request.user),
                "edited": edited,
            },
        )


class EventToggleAttendance(TemplateView):
    def get(self, request, eventId=None) -> HttpResponse:

        event = Event.objects.get(id=eventId)

        if not event.current_user_is_part_of_event(request.user):
            event.attendees.add(request.user)

        else:
            event.attendees.remove(request.user)

        return redirect("/workshops/" + str(event.id))
