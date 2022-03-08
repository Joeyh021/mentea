from .models import User, MentorMentee


def get_mentor(mentee: User) -> User:
    relationship = MentorMentee.objects.get(mentee=mentee)
    return User.objects.get(id=relationship.mentor.id)


def mentor_mentors_mentee(mentor: User, mentee: User) -> bool:
    return MentorMentee.objects.filter(mentee=mentee, mentor=mentor, approved=True).exists()