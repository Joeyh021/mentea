from .models import Event
from django import forms
from django.forms import TextInput




class WorkshopForm(forms.Form):
    
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
        
    )
    startTime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    desc = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"})
    )
    
    class Meta:
        model = Event
        fields = ('name','startTime','duration',)
    
