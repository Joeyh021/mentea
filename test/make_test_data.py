from subprocess import call
from uuid import uuid4
from people import models
from django.core.management import call_command

# has to be imported and run from `manage.py shell`
# from test.make_test_data import create_data; create_data()


def create_data() -> None:

    # create user types
    mentee_type = models.UserType.objects.create(id=uuid4(), type="mentee")
    mentor_type = models.UserType.objects.create(id=uuid4(), type="mentor")
    mentor_mentee_type = models.UserType.objects.create(
        id=uuid4(), type="mentor mentee"
    )
    none_usertype = models.UserType.objects.create(id=uuid4(), type="")

    # create some business areas
    money_laundering = models.BusinessArea.objects.create(
        id=uuid4(), business_area="money laundering"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Russian_money-laundering,_2017
    tax_evasion = models.BusinessArea.objects.create(
        id=uuid4(), business_area="tax evasion"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Tax_evasion,_2016
    global_economy_manipulation = models.BusinessArea.objects.create(
        id=uuid4(), business_area="global economy manipulation"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Role_in_Financial_crisis_of_2007%E2%80%932008
    financing_nonces = models.BusinessArea.objects.create(
        id=uuid4(), business_area="financing paedophiles"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Fine_for_business_with_Jeffrey_Epstein,_2020

    # create some mentors
    models.User.objects.create(
        id=uuid4(),
        first_name="John",
        last_name="Mentor",
        email="john@gmail.com",
        business_area=money_laundering,
        bio="",
        user_type=mentor_type,
    )
    # create some mentees
    models.User.objects.create(
        id=uuid4(),
        first_name="Tim",
        last_name="Mentee",
        email="tim@db.com",
        business_area=money_laundering,
        bio="",
        user_type=mentee_type,
    )
