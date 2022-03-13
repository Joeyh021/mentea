from django.test.client import Client
import pytest
from people.models import *
from pytest_django import asserts

pytestmark = pytest.mark.django_db()


def test_mentee_dashboard(client: Client, mentee: User):
    """Test the dashboard has all the data in it's right place"""
    response = client.get("/mentee/")
    asserts.assertTemplateUsed(response, "people/mentee_dashboard.html")

    # our mentor should be "Test Mentor"
    mentor = response.context["mentor"]
    assert mentor.first_name == "Test"

    # meeting should show up on dashboard
    meeting = response.context["upcoming_meetings"].get()
    assert meeting.name == "Meeting"

    # as should plan of action
    plan = response.context["plans"].get()
    assert plan.name == "test plan"


def test_feedback(client: Client, mentee: User):
    """Test that we can see feedback"""
    response = client.get("/mentee/view_general_feedback/")
    asserts.assertTemplateUsed(response, "people/mentee_view_general_feedback.html")
    assert "dumb and complains" in response.context["ff"][0].feedback
