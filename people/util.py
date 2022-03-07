from .models import User, MentorMentee
from events.models import Event
from datetime import datetime


def get_mentor(mentee: User) -> User:
    relationship = MentorMentee.objects.get(mentee=mentee)
    return User.objects.get(id=relationship.mentor.id)
