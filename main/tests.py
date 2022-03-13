"""Tests for app main"""
from django.test.client import Client
from pytest_django import asserts


def test_main_index_page(client: Client):
    """test index page returns correct template"""
    response = client.get("/")
    asserts.assertTemplateUsed(response, "main/index.html")


def test_faq_page(client: Client):
    """test faq page returns correct template"""
    response = client.get("/faq/")
    asserts.assertTemplateUsed(response, "main/faq.html")


def test_feedback_page(client: Client):
    """test feedback page returns correct template"""
    response = client.get("/feedback/")
    asserts.assertTemplateUsed(response, "main/feedback.html")


def test_privacy_page(client: Client):
    """test privacy page returns correct template"""
    response = client.get("/privacy/")
    asserts.assertTemplateUsed(response, "main/privacy.html")


def test_tos_page(client: Client):
    """test terms of service page returns correct template"""
    response = client.get("/terms-of-service/")
    asserts.assertTemplateUsed(response, "main/tos.html")


def test_feedback_form(client: Client):
    """Test feedback form works correctly"""
    # NOAH: TODO
    pass
