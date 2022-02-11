import models
from typing import List, Tuple
import uuid


def get_matches(mentee_id: uuid.UUID) -> List[uuid.UUID]:
    """given the uuid of a mentee, find the best possible mentors, returning a list of their uuids in order of suitability"""
    mentee: models.User = models.User.objects.get(id=mentee_id)
    suitable_mentors = list(
        models.User.objects.filter(
            user_type="mentor",
        ).exclude(business_area=mentee.business_area)
    )
    # number of mentees the mentor has
    # score from 1 to 0 of how much their interests overlap
    # 0 for none 1 for all
    mentor_scores: List[Tuple[uuid.UUID, int]] = []
    for mentor in suitable_mentors:
        pass
        # calculate the normalised number of shared topics (number they share / number of mentee topics)
        # multiply by some constant, maybe dependant upon the number of mentors in the system
        # factor in ratings here - maybe times by average rating between 0 and 1?
        # add to the mentors current number of mentors + number of workshops scheduled * some constant (0.2 ish?)
    return []
