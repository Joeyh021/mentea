from django import forms

from .models import BusinessArea, Topic


class ProfileForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)
    business_area = forms.ModelChoiceField(
        queryset=BusinessArea.objects.all()
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all()
    )
