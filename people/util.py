from .models import User, MentorMentee


def get_mentor(mentee: User) -> User:
    relationship = MentorMentee.objects.get(mentee=mentee)
    return User.objects.get(id=relationship.mentor)
