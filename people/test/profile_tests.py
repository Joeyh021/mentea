from django.test.client import Client
from pytest_django import asserts
from people.models import *
import pytest
import random


pytestmark = pytest.mark.django_db()


def test_user_profile_page_mentee(client: Client, mentee: User):
    """Test a mentee can view their profile and that it has the correct info"""
    response = client.get("/user/profile/")
    asserts.assertTemplateUsed(response, "people/profile.html")
    mentee_topics = UserTopic.objects.filter(user=mentee, usertype=UserType.Mentee)
    print(mentee_topics)
    print(response.context["mentee_topics"])
    assert list(response.context["mentee_topics"]) == list(mentee_topics)
    assert b"I am a mentee" in response.content


def test_user_profile_page_mentor(client: Client, mentor: User):
    """Test a mentee can view their profile and that it has the correct info"""
    response = client.get("/user/profile/")
    asserts.assertTemplateUsed(response, "people/profile.html")
    mentor_topics = UserTopic.objects.filter(user=mentor, usertype=UserType.Mentor)
    print(mentor_topics)
    print(response.context["mentor_topics"])
    assert list(response.context["mentor_topics"]) == list(mentor_topics)
    assert b"I am a mentor" in response.content


def test_edit_profile(client: Client, mentor: User):
    """Test a user can edit their profile and that the changes are reflected"""
    response = client.get("/user/profile/edit/")
    asserts.assertTemplateUsed(response, "people/profile_edit.html")
    # create new profile data
    new_business_area = random.choice(list(BusinessArea.objects.all()))
    new_mentee_topics = random.sample(list(Topic.objects.all()), 2)
    new_mentor_topics = random.sample(list(Topic.objects.all()), 2)
    data = {
        "usertype": ["MentorMentee"],
        "bio": ["About me"],
        "mentee_topics": new_mentee_topics,
        "mentor_topics": new_mentor_topics,
        "business_area": new_business_area,
    }
    response = client.post("/user/profile/edit", data=data)
    print(response.content)
    assert mentor.user_type == "MentorMentee"


def test_add_topics(client: Client, mentor: User):
    "Test a user can add new topics"
    # make sure we can see page
    response = client.get("/user/profile/edit/")
    asserts.assertTemplateUsed(response, "people/profile_edit.html")
    # create some data and post it
    data = {"topic_new": ["New Topic!"]}
    response = client.post("/user/profile/edit/", data=data)
    assert Topic.objects.filter(topic="New Topic!").exists()


def test_add_business_area(client: Client, mentee: User):
    "Test a user can add new topics"
    # make sure we can see page
    response = client.get("/user/profile/edit/")
    asserts.assertTemplateUsed(response, "people/profile_edit.html")
    # create some data and post it
    data = {"business_area_new": ["Very Important Business"]}
    response = client.post("/user/profile/edit/", data=data)
    assert BusinessArea.objects.filter(business_area="Very Important Business").exists()
