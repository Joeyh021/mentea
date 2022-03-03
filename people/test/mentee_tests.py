from django.test.client import Client
from pytest_django import asserts
import pytest


pytestmark = pytest.mark.django_db()


def test_mentee_dashboard_page(client: Client, mentee) -> None:
    response = client.get("/mentee/")
    asserts.assertTemplateUsed(response, "people/mentee_dashboard.html")
