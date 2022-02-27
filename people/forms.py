from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.firstname = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


from .models import BusinessArea, Topic, UserType


class ProfileForm(forms.Form):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"})
    )
    business_area = forms.ModelChoiceField(
        queryset=BusinessArea.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    mentee_topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )
    mentor_topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )
    usertype = forms.ChoiceField(
        choices=UserType.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class BusinessAreaForm(forms.Form):
    business_area_new = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )


class TopicForm(forms.Form):
    topic_new = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
