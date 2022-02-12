from django.core.management import call_command
import pytest
from test.make_test_data import create_data

# populate the test database with some basic data from test_data.json


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):  # type: ignore
    """overriden db setup fixture that loads the test data from a json file"""
    with django_db_blocker.unblock():
        create_data()
