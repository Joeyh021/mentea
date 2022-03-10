from people.matching import get_matches
from people.models import *
import pytest
from django.test.client import Client


pytestmark = pytest.mark.django_db()

# also TODO. There is much TODO.
# shouldnt actually be too hard to do once I sit down and figure it out.


def test_workshops_page(client: Client, mentee: User):
    pass
