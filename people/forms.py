from django import forms

from .models import BusinessArea, Topic


class ProfileForm(forms.Form):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"})
    )
    business_area = forms.ModelChoiceField(
        queryset=BusinessArea.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.Select(attrs={"class": "form-select", "multiple": "multiple"}),
    )
