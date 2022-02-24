


from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from typing import Any
from django.contrib import messages

from events.forms import WorkshopForm

from .models import Event, EventType





class EventsIndexPage(TemplateView):
    """
    The main workshops page, containing a list of all currently scheduled workshops and links to their individual pages.
    Should also contain UI to link to /create (if authenticated as mentor), and to /request (if authenticated as mentee)
    """

    template_name = "workshops/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


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
            initial={
                "mentor": request.user.id
            }
        )
        return render(request, self.template_name, {"form": form})
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            # Get current user (a mentor)
            
            formData = form.cleaned_data
            
            etype = EventType.objects.get(name="WORKSHOP")
            
            event = Event(name=formData['name'], startTime=formData['startTime'], duration=formData['duration'], location="Online", mentor=request.user, type=etype, description=formData['desc'])
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
        
        return render(request, self.template_name, {"event": event})
