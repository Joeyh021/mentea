from django.test.client import Client
import pytest
from people.models import *
from pytest_django import asserts

pytestmark = pytest.mark.django_db()


def test_mentor_dashboard(client: Client, mentor: User):
    """Test the dashboard has all the data in it's right place"""
    response = client.get("/mentor/")
    asserts.assertTemplateUsed(response, "people/mentor_dashboard.html")

    # our mentor should be "Test Mentor"
    mentee = response.context["mentees"].get().mentee
    assert mentee.last_name == "Mentee"

    # meeting should show up on dashboard
    meeting = response.context["upcoming_meetings"].get()
    assert meeting.event.name == "Meeting"


def test_mentor_mentee_page(client: Client, mentor: User):
    """Test our mentee overview has all the data in it's right place"""
    test_mentee = User.objects.get(last_name="Mentee")
    response = client.get(f"/mentor/mentees/{test_mentee.id}/")
    asserts.assertTemplateUsed(response, "mentor_mentee/relationship.html")

    # do we have the right mentee?
    mentee = response.context["mentee"]
    assert mentee == test_mentee

    # meeting should be here too
    meeting = response.context["meetings"].get()
    assert meeting.event.name == "Meeting"

    # as should plan of action
    plan = response.context["relation"].get_plans_of_action()[0]
    assert plan.name == "test plan"


def test_feedback(client: Client, mentor: User):
    """Test that we can see feedback"""
    response = client.get("/mentor/view_general_feedback/")
    asserts.assertTemplateUsed(response, "people/mentor_view_general_feedback.html")
    assert "knows nothing and is boring" in response.context["ff"][0].feedback
