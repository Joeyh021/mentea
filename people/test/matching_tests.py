from people.matching import get_matches
from people.models import *
import pytest

pytestmark = pytest.mark.django_db()


@pytest.mark.dependency()
def test_matching_data() -> None:
    """Test the matching algorithm can pull the correct data from the database"""
    # make sure tim is okay
    tim = User.objects.get(first_name="Tim", last_name="Mentee")
    # make sure that the algo runs without fail before we try to check ordering and stuff
    get_matches(tim.id)


@pytest.mark.dependency(depends=["test_matching_data"])
def test_matches_1() -> None:
    """Test the matches are returned in the order expected"""
    # get a test mente
    # run the matching algo
    # make sure that all mentors in the dataset are in the order we expect


# maybe like a couple of these
