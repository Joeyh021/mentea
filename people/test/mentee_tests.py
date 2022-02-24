from django.test.client import Client
from pytest_django import asserts


def test_mentee_dashboard_page(client: Client) -> None:
    pass
    # response = client.get("/mentee/")
    # asserts.assertTemplateUsed(response, "people/mentee_dashboard.html")
    # TODO:  add some assertions about the template contexts here once those are done
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#assertions
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#testing-responses
