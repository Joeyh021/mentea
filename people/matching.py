from people.models import *
from events.models import Event


def get_matches(mentee: User):
    """
    given the uuid of a mentee, find the best possible mentors, returning a list of their uuids in order of suitability
    if debug, then a dict of the calculated values is returned for testing/debugging purposes
    """
    mentee_type = UserType.Mentee
    mentor_mentee_type = UserType.MentorMentee
    mentor_type = UserType.Mentor

    mentee_topics = [ut.topic for ut in UserTopic.objects.filter(user=mentee)]
    all_mentors = list(
        User.objects.filter(user_type=mentor_type)
        .exclude(business_area=mentee.business_area)
        .union(
            User.objects.filter(user_type=mentor_mentee_type).exclude(
                business_area=mentee.business_area
            )
        )
    )

    total_n_mentees = len(
        User.objects.filter(user_type=mentee_type).union(
            User.objects.filter(user_type=mentor_mentee_type)
        )
    )

    total_n_events = len(Event.objects.all())

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
        mentees_score = (
            (len(MentorMentee.objects.filter(mentor=mentor)) / total_n_mentees)
            if total_n_mentees != 0
            else 0
        )

        events_score = (
            (len(Event.objects.filter(mentor=mentor)) / total_n_events)
            if total_n_events != 0
            else 0
        )

        # final score is some linear combination of these 4 parameters
        # workload scores are * (1-score), topic overlap score is the main factor
        # designed to decrease score if the mentor is busy compared to other mentors
        score = (
            topic_overlap_score
            * average_rating
            * (1 - mentees_score)
            * (1 - events_score)
        )
        mentor_scores.append((mentor, score))

    mentor_scores.sort(key=lambda t: t[1], reverse=True)
    return mentor_scores
