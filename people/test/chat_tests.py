from django.test.client import Client
from pytest_django import asserts
import pytest
from people.models import *

pytestmark = pytest.mark.django_db()


def test_mentor_send_chat(client: Client, mentor: User):
    """Test a mentor can send a chat and mentee recieve it"""
    pass


def test_mentee_send_chat(client: Client, mentor: User):
    """Same as above but vice-versa"""
    pass
