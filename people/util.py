from .models import User, MentorMentee
from events.models import Event
from datetime import datetime


def get_mentor(mentee: User) -> User:
    relationship = MentorMentee.objects.get(mentee=mentee)
    return User.objects.get(id=relationship.mentor.id)

def get_meeting_request(mentee: User, start_time: datetime) -> Event:
    event = Event.objects.get(mentee=mentee, start_time=start_time)
    return MeetingRequest.objects.get(eventid=event.id)
