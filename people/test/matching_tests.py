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
    """Test the matches are returned in the order expected with the scores expected"""
    # testing tim here
    tim = User.objects.get(first_name="Tim", last_name="Mentee")
    matches = get_matches(tim)

    # overlap score is 1.0
    # minus 0.125 because steve already has one mentor (Joey)
    assert matches[0] == (User.objects.get(first_name="Steve"), pytest.approx(0.875))
    # should be 3 matches total - all those not in the money laundering department
    assert len(matches) == 3


@pytest.mark.dependency(depends=["test_matching_data"])
def test_matches_2() -> None:
    """Test the matches are returned in the order expected with the scores expected"""
    # testing sandra here
    sandra = User.objects.get(first_name="Sandra")
    matches = get_matches(sandra)

    # gonna look at top two with overlap - john and joey
    # john has an overlap score of 0.25
    # joey has an overlap score of 0.5
    # joey also has terrible reviews, bringing his score down to 0.1
    # joey also has a mentee already, bringing his score down further to 0.0875
    # minus 0.125 because john already has one mentor (Joey)
    assert matches[0] == (User.objects.get(first_name="John"), pytest.approx(0.25))
    assert matches[1] == (User.objects.get(first_name="Joey"), pytest.approx(0.0875))
    # should be 5 matches total - no one else works in noncing at the moment
    assert len(matches) == 5


@pytest.mark.dependency(depends=["test_matching_data"])
def test_matches_3() -> None:
    """Test the matches are returned in the order expected with the scores expected"""
    # testing sandra here
    sandra = User.objects.get(first_name="Sandra")
    matches = get_matches(sandra)

    # gonna look at top two with overlap - john and joey
    # john has an overlap score of 0.25
    # joey has an overlap score of 0.5
    # joey also has terrible reviews, bringing his score down to 0.1
    # joey also has a mentee already, bringing his score down further to 0.0875
    # minus 0.125 because john already has one mentor (Joey)
    assert matches[0] == (User.objects.get(first_name="John"), pytest.approx(0.25))
    assert matches[1] == (User.objects.get(first_name="Joey"), pytest.approx(0.0875))
    # should be 5 matches total - no one else works in noncing at the moment
    assert len(matches) == 5
