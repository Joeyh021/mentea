from uuid import uuid4
import pytest
from people import models

# tells django the tests need a db
pytestmark = pytest.mark.django_db()


def test_db_loaded() -> None:
    mentee: models.User = models.User.objects.get(first_name="Tim")
    assert mentee.last_name == "Mentee"
