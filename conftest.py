# type: ignore
import pytest
from tests.test_data import create_data

# populate the test database with some basic data from test_data.json


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """overriden db setup fixture that loads the test data from a json file"""
    with django_db_blocker.unblock():
        create_data()
