from email import message
from django.test.client import Client
from pytest_django import asserts
import pytest
from people.models import *

pytestmark = pytest.mark.django_db()


def test_send_and_receive_chat(client: Client):
    """Test a mentor and mentee can send and recieve chat"""
    # login manually so we can log in and out of mentee and mentor
    client.login(email="mentee@mentea.me", password="menteepass")
    mentee = User.objects.get(email="mentee@mentea.me")

    # test can see chat page
    response = client.get("/mentee/chat/")
    # can we see the messages already there?
    messages = list(response.context["chatMessages"])
    assert messages[0].content == "What is your favourite colour?"
    assert messages[1].sender == mentee

    # send new message
    client.post("/mentee/chat/", data={"content": "Wait, no, yellow!"})
    # can we see it?
    response = client.get("/mentee/chat/")
    assert list(response.context["chatMessages"])[2].content == "Wait, no, yellow!"

    client.logout()
    client.login(email="mentor@mentea.me", password="mentorpass")
    mentor = User.objects.get(email="mentor@mentea.me")

    # can the mentor see it?
    response = client.get(f"/mentor/{mentee.id}/chat/")
    messages = list(response.context["chatMessage"])
    assert [m.content for m in messages] == [
        "What is your favourite colour?",
        "Blue",
        "Wait, no, yellow!",
    ]
    assert messages[2].sender == mentee
