# type: ignore
import pytest
from tests.test_data import create_default_data
from people.models import User

# populate the test database with some basic data from test_data.json


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """overriden db setup fixture that loads the test data"""
    with django_db_blocker.unblock():
        create_default_data()


@pytest.fixture(scope="function")
def mentee(client):
    client.login(email="mentee@mentea.me", password="menteepassword")
    return User.objects.get(email="mentee@mentea.me")


@pytest.fixture(scope="function")
def mentor(client):
    client.login(email="mentor@mentea.me", password="mentorpassword")
    return User.objects.get(email="mentor@mentea.me")
