from people.matching import get_matches
from people.models import *
from events.models import *
import pytest
from django.test.client import Client
from datetime import datetime, timedelta

pytestmark = pytest.mark.django_db()

# also TODO. There is much TODO.
# shouldnt actually be too hard to do once I sit down and figure it out.


def test_index_page_mentee(client: Client, mentee: User):
    """Test a mentee can view the index page and it has the correct content"""
    response = client.get("/workshops/")
    all_workshops = response.context["page_obj"].object_list
    assert all_workshops[0].name == "Test Event"
    assert response.context["my_events"][0].name == "Test Event"


def test_mentee_signup(client: Client, mentee: User):
    """Test a mentee can toggle signups for an existing event"""
    workshop = Event.objects.get(name="Test Event")
    response = client.get(f"/workshops/{workshop.id}/")
    assert response.context["registeredToEvent"] == True
    client.get(f"/workshops/{workshop.id}/toggleAttendance")
    response = client.get(f"/workshops/{workshop.id}/")
    assert response.context["registeredToEvent"] == False


def test_view_previous_workshops(client: Client, mentee: User):
    """Test a user can view workshops they previously attended"""
    response = client.get("/workshops/previous/")
    print(Event.objects.get(name="Test Event 2").attendees)
    prev_workshops = response.context["page_obj"].object_list
    assert prev_workshops[0].name == "Test Event 2"


def test_index_page_mentor(client: Client, mentor: User):
    """Test a mentor can view the index page and it has the correct content"""
    response = client.get("/workshops/")
    all_workshops = response.context["page_obj"].object_list
    assert all_workshops[0].name == "Test Event"


def test_create_workshop(client: Client, mentor: User):
    """Test a mentor can create a new workshop"""
    topic = Topic.objects.get(topic="python programming")
    data = {
        "name": "Super Epic New Workshop",
        "startTime": str(datetime.now() + timedelta(hours=4)),
        "duration": 60,
        "topic": topic.id,
        "description": "how not to manage a group project",
    }
    response = client.post("/workshops/create/", data=data)
    print(response)
    assert Event.objects.filter(name="Super Epic New Workshop").exists()


def test_delete_workshop(client: Client, mentor: User):
    """Test a workshop can be deleted"""
    event = Event.objects.get(name="Test Event")
    response = client.post(f"/workshops/{event.id}/delete")
    assert response.status_code == 302
    assert Event.objects.filter(name="Test Event").exists() == False
