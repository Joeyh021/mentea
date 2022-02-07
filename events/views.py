from django.shortcuts import render
from django.views.generic import TemplateView


class EventsIndexPage(TemplateView):
    """
    The main workshops page, containing a list of all currently scheduled workshops and links to their individual pages.
    Should also contain UI to link to /create (if authenticated as mentor), and to /request (if authenticated as mentee)
    """

    template_name = "workshops/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class EventRequestPage(TemplateView):
    """
    Mentees should be able to express interest in a new workshop around a specific topic here.
    """

    template_name = "workshops/request.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class EventCreatePage(TemplateView):
    """
    Mentors should be able to see what topics are frequently requested and schedule new workshops here.
    """

    template_name = "workshops/create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class EventPage(TemplateView):
    """
    A page for each event, containing info about the event, whos running it, attendees, and anything else.
    """

    # not sure what best practice is for this template name
    template_name = "workshops/event.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
