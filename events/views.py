


from datetime import datetime, timedelta, timezone
import json
from typing_extensions import Required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from events.forms import WorkshopForm
from people.models import Topic

from .models import Event, EventAttendee, EventType, FeedbackForm, Questions

from django.core.paginator import Paginator
from django.db.models import F




class EventsIndexPage(LoginRequiredMixin, TemplateView):
    """
    The main workshops page, containing a list of all currently scheduled workshops and links to their individual pages.
    Should also contain UI to link to /create (if authenticated as mentor), and to /request (if authenticated as mentee)
    """

    template_name = "workshops/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        
        my_events = request.user.eusers.order_by("startTime").filter(endTime__gte=datetime.now()).all()
        my_running_events = Event.objects.filter(mentor=request.user, endTime__gte=datetime.now())
        
        #return HttpResponse(my_events)
        
        event_list = Event.objects.order_by("startTime").filter(endTime__gte=datetime.now()).all()
        paginator = Paginator(event_list, 9)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, self.template_name, {'page_obj': page_obj, 'my_events': my_events.union(my_running_events)})
    
class EventsPreviousPage(LoginRequiredMixin, TemplateView):
    """
    The main workshops page, containing a list of all currently scheduled workshops and links to their individual pages.
    Should also contain UI to link to /create (if authenticated as mentor), and to /request (if authenticated as mentee)
    """

    template_name = "workshops/previous.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        
        my_events = request.user.eusers.order_by("startTime").filter(endTime__lte=datetime.now()).all()
        my_running_events = Event.objects.order_by("startTime").filter(mentor=request.user, endTime__lte=datetime.now())
        
        #return HttpResponse(my_events)
        

        paginator = Paginator(my_events.union(my_running_events), 9)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, self.template_name, {'page_obj': page_obj})


class EventRequestPage(TemplateView):
    """
    Mentees should be able to express interest in a new workshop around a specific topic here.
    """

    template_name = "workshops/request.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class EventCreatePage(TemplateView):
    """
    Mentors should be able to see what topics are frequently requested and schedule new workshops here.
    """

    template_name = "workshops/create.html"
    
    form_class: Any = WorkshopForm

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        form = self.form_class(
      
        )
        return render(request, self.template_name, {"form": form})
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            # Get current user (a mentor)
            
            formData = form.cleaned_data
            
            etype = EventType.objects.get(name="WORKSHOP")
            
            startTime = formData["startTime"]
            endTime = startTime + timedelta(minutes = formData["duration"])
            
            event = Event(name=formData['name'], startTime=formData['startTime'], endTime=endTime, duration=formData['duration'], location="Online", mentor=request.user, type=etype, description=formData['desc'], topic=formData['topic'])
            event.save()
            
            
            # Build form here
            ff = FeedbackForm(name="Feedback for " + event.name, desc="Please fill out this form honestly! It can only be submitted once!", allowsMultipleSubmissions=False, allowsEditingSubmissions=False)
            ff.save()
            
            q_data = json.loads('{"options": [{"key": "Yes", "value": "dc9ba51f-d768-48f4-905f-a8a458a459b9"}, {"key": "No", "value": "278f8734-69f7-48ae-8a9b-f5efc9fa9f17"}]}')
            
            q1 = Questions(name="Did you enjoy the workshop?", form=ff, type="select", required=True, order=0, type_data=q_data)
            q1.save()
            
            q2 = Questions(name="General Feedback", form=ff, required=False, order=1, type="textarea", type_data="")
            q2.save()
            
            event.feedback_form = ff
            event.save()
            
            return redirect("/workshops/"+ str(event.id)+"/")
            
       
        else:
            messages.error(request, "Error creating workshop!")
            return render(request, self.template_name, { "form": form})
        


class EventPage(TemplateView):
    """
    A page for each event, containing info about the event, whos running it, attendees, and anything else.
    """

    # not sure what best practice is for this template name
    template_name = "workshops/event.html"

    def get(self, request: HttpRequest, eventId=None) -> HttpResponse:
        
        event = Event.objects.get(id=eventId)
        
        userHasJoined = event.current_user_is_part_of_event(request.user)
        
        return render(request, self.template_name, {"event": event, "registeredToEvent": userHasJoined, "isMentor": event.current_user_is_mentor(request.user)})

class EventToggleAttendance(TemplateView):
    def get(self, request, eventId=None) -> HttpResponse:
        
        event = Event.objects.get(id=eventId)
        
        if not event.current_user_is_part_of_event(request.user):
            event.attendees.add(request.user)
            
        else:
            event.attendees.remove(request.user)
            
        return redirect("/workshops/"+str(event.id))