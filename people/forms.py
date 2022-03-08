from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, BusinessArea, Topic, UserType


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
        user.user_type = "None"
        if commit:
            user.save()
        return user


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


class PlanOfActionForm(forms.Form):
    name = forms.CharField(
        label="Plan Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    #
    target_1 = forms.CharField(
        label="Target",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    target_2 = forms.CharField(
        label="Target",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    target_3 = forms.CharField(
        label="Target",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    target_4 = forms.CharField(
        label="Target",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    target_5 = forms.CharField(
        label="Target",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # Change this to be all mentors with a relationship to the mentee.
    mentor = forms.ModelChoiceField(queryset=User.objects.all())
    description_1 = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"}),
    )
    description_2 = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"}),
    )
    description_3 = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"}),
    )
    description_4 = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"}),
    )
    description_5 = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control"}),
    )



class CreateMeetingForm(forms.Form):
    name = forms.CharField(widget=forms.Textarea)
    start_time = forms.DateTimeField()
    location = forms.CharField(widget=forms.Textarea)
    duration = forms.IntegerField()


class MenteeRescheduleForm(forms.Form):
    start_time = forms.DateTimeField()
    location = forms.CharField(widget=forms.Textarea)
    duration = forms.IntegerField()


class SendMessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))



class MentorRescheduleForm(forms.Form):
    start_time = forms.DateTimeField()
    location = forms.CharField(widget=forms.Textarea)
    duration = forms.IntegerField()


class CreateMeetingNotesForm(forms.Form):
    content = forms.CharField(max_length=500)

