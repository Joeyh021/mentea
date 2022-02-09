from django.test.client import Client
from pytest_django import asserts


def test_main_index_page(client: Client) -> None:
    response = client.get("/")
    asserts.assertTemplateUsed(response, "main/inde.html")
