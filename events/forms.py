from attr import attrs

from people.models import Topic
from .models import Event, EventRequest
from django import forms
from django.forms import TextInput


class WorkshopForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    startTime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    desc = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"})
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Event
        fields = (
            "name",
            "startTime",
            "duration",
        )


class WorkshopRequestForm(forms.Form):

    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = EventRequest
        fields = ("topic",)
