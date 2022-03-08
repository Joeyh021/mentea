from typing import Tuple
from .models import User, MentorMentee
from events.models import Event
from datetime import datetime


def get_mentor(mentee: User) -> User:
    relationship = MentorMentee.objects.get(mentee=mentee)
    return User.objects.get(id=relationship.mentor.id)


def mentor_mentors_mentee(mentor: User, mentee: User) -> Tuple[bool, MentorMentee]:
    try:
        return (True, MentorMentee.objects.get(mentee=mentee, mentor=mentor, approved=True))
    except:
        return (False, None)
    
