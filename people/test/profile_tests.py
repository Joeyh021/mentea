from django.test.client import Client
from pytest_django import asserts


def test_user_profile_page(client: Client) -> None:
    response = client.get("/user/profile/")
    asserts.assertTemplateUsed(response, "people/profile.html")
    # TODO:  add some assertions about the template contexts here once those are done
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#assertions
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#testing-responses
