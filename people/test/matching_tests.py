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
    get_matches(tim)


@pytest.mark.dependency(depends=["test_matching_data"])
def test_matches_1() -> None:
    """Test the matches are returned in the order expected"""
    tim = User.objects.get(first_name="Tim", last_name="Mentee")
    matches = get_matches(tim)

    # steve should be the top match because the topics overlap
    assert matches[0] == User.objects.get(first_name="Steve")
    assert len(matches) == 2


# maybe like a couple of these
