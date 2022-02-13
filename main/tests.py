from django.test.client import Client
from pytest_django import asserts


def test_main_index_page(client: Client) -> None:
    response = client.get("/")
    asserts.assertTemplateUsed(response, "main/index.html")
    # TODO: add some assertions about the template contexts here once those are done
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#assertions
    # https://docs.djangoproject.com/en/4.0/topics/testing/tools/#testing-responses


def test_faq_page(client: Client) -> None:
    response = client.get("/faq/")
    asserts.assertTemplateUsed(response, "main/faq.html")


def test_feedback_page(client: Client) -> None:
    response = client.get("/feedback/")
    asserts.assertTemplateUsed(response, "main/feedback.html")


def test_privacy_page(client: Client) -> None:
    response = client.get("/privacy/")
    asserts.assertTemplateUsed(response, "main/privacy.html")


def test_tos_page(client: Client) -> None:
    response = client.get("/terms-of-service/")
    asserts.assertTemplateUsed(response, "main/tos.html")
