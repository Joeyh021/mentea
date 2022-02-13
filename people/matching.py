from typing import List, Tuple
import uuid

from people.models import *
from events.models import Event


def get_matches(mentee: User) -> List[User]:
    """given the uuid of a mentee, find the best possible mentors, returning a list of their uuids in order of suitability"""
    mentor_type = UserType.objects.get(type="mentor")

    mentee_topics = [ut.topic for ut in UserTopic.objects.filter(user=mentee)]
    all_mentors: List[User] = list(
        User.objects.filter(user_type=mentor_type).exclude(
            business_area=mentee.business_area
        )
    )

    mentor_scores: List[Tuple[User, float]] = []
    for mentor in all_mentors:
        # get topic overlap
        mentor_topics = [ut.topic for ut in UserTopic.objects.filter(user=mentor)]
        topic_overlap = [t for t in mentee_topics if t in mentor_topics]  # intersection
        # normalised 0 to 1
        topic_overlap_score = len(topic_overlap) / len(mentee_topics)

        # get mentor ratings
        mentor_ratings = [r.rating for r in Rating.objects.filter(mentor=mentor)]

        # just use average of all for now - can maybe add more nuance later (TODO)
        # assume ratings are 0 <= r <= 5 to normalise 0 to 1
        if len(mentor_ratings) == 0:
            average_rating = 0.0
        else:
            average_rating = sum(mentor_ratings) / len(mentor_ratings) / 5

        score = average_rating * topic_overlap_score

        # calculate workload
        n_mentees = len(MentorMentee.objects.filter(mentor=mentor))
        n_workshops = len(Event.objects.filter(mentor=mentor))

        # factor determines how weighted workshops are in calculating a mentors workload
        workshop_workload_factor = 0.1
        workload = n_mentees + n_workshops * workshop_workload_factor

        # score factore determines how much the score should be weighted
        score_factor = 5
        score += workload + score * score_factor

        mentor_scores.append((mentor, score))

    mentor_scores.sort(key=lambda t: t[1], reverse=True)
    return [t[0] for t in mentor_scores]
