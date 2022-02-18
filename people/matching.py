from typing import Any, List, Tuple, Union, Dict

from people.models import *
from events.models import Event


def get_matches(mentee: User):
    """
    given the uuid of a mentee, find the best possible mentors, returning a list of their uuids in order of suitability
    if debug, then a dict of the calculated values is returned for testing/debugging purposes
    """
    mentor_type = UserType.objects.get(type="mentor")
    mentor_mentee_type = UserType.objects.get(type="mentor mentee")

    mentee_topics = [ut.topic for ut in UserTopic.objects.filter(user=mentee)]
    all_mentors: List[User] = list(
        User.objects.filter(user_type=mentor_type).exclude(
            business_area=mentee.business_area
        )
    )
    # add in users that are mentors and mentees
    all_mentors += list(
        User.objects.filter(user_type=mentor_mentee_type).exclude(
            business_area=mentee.business_area
        )
    )

    mentor_scores = []
    for mentor in all_mentors:
        # get topic overlap
        # account for where mentor_mentee users have topics marked as their mentoring topics
        if mentor.user_type == mentor_type:
            mentor_topics = [ut.topic for ut in UserTopic.objects.filter(user=mentor)]
        else:
            mentor_topics = [
                ut.topic
                for ut in UserTopic.objects.filter(user=mentor, usertype=mentor_type)
            ]

        topic_overlap = [t for t in mentee_topics if t in mentor_topics]  # intersection
        # normalised 0 to 1
        topic_overlap_score = len(topic_overlap) / len(mentee_topics)

        # get mentor ratings
        mentor_ratings = [r.rating for r in Rating.objects.filter(mentor=mentor)]

        # just use average of all for now - can maybe add more nuance later (TODO)
        # assume ratings are 0 <= r <= 5 to normalise 0 to 1
        if len(mentor_ratings) == 0:
            average_rating = 1.0  # if no ratings then just ignore
        else:
            average_rating = sum(mentor_ratings) / len(mentor_ratings) / 5

        # calculate workload
        n_mentees = len(MentorMentee.objects.filter(mentor=mentor))
        n_workshops = len(Event.objects.filter(mentor=mentor))

        # factor determines how weighted workshops are in calculating a mentors workload
        workshop_workload_factor = 0.1
        workload = n_mentees + n_workshops * workshop_workload_factor

        score = 1.0  # some computation that is a factor of the things calculated
        mentor_scores.append((mentor, score))

        mentor_scores.sort(key=lambda t: t[1], reverse=True)
        return [t[0] for t in mentor_scores]
