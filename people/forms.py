from django import forms

from .models import BusinessArea, UserTopic


class ProfileForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)
    business_area = forms.ModelChoiceField(
        queryset=BusinessArea.objects.all(), to_field_name="business_area"
    )  # What we want this to do is select all business areas we have in the system (which it does), and show the actual business area name, which it does not
    topics = forms.ModelMultipleChoiceField(
        queryset=UserTopic.objects.all(), to_field_name="user_topics"
    )  # Similar to above but for topics
