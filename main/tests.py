from django.test.client import Client
from pytest_django import asserts


def test_main_index_page(client: Client) -> None:
    response = client.get("/")
    asserts.assertTemplateUsed(response, "main/index.html")
    # add some assertions about the template contexts here once those are done
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#assertions
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#testing-responses


def test_faq_page(client: Client) -> None:
    response = client.get("faq/")
    asserts.assertTemplateNotUsed(response, "main/faq.html")
    # TODO: change this from NotUsed when the template gets written
