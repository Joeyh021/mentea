from uuid import uuid4
from people.models import *


def create_data() -> None:

    # create user types
    mentee_type = UserType.objects.create(type="mentee")
    mentor_type = UserType.objects.create(type="mentor")
    mentor_mentee_type = UserType.objects.create(type="mentor mentee")
    none_usertype = UserType.objects.create(type="")

    # create some business areas
    money_laundering = BusinessArea.objects.create(
        business_area="money laundering"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Russian_money-laundering,_2017
    tax_evasion = BusinessArea.objects.create(
        business_area="tax evasion"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Tax_evasion,_2016
    global_economy_manipulation = BusinessArea.objects.create(
        business_area="global economy manipulation"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Role_in_Financial_crisis_of_2007%E2%80%932008
    financing_nonces = BusinessArea.objects.create(
        business_area="financing paedophiles"
    )  # https://en.wikipedia.org/wiki/Deutsche_Bank#Fine_for_business_with_Jeffrey_Epstein,_2020

    # create a bunch of topics that our bankers may be interested in
    making_money = Topic.objects.create(topic="making money")
    stonks = Topic.objects.create(topic="stonks")
    crypto = Topic.objects.create(topic="cryptocurrency")
    management = Topic.objects.create(topic="project management")
    spreadsheets = Topic.objects.create(topic="excel spreadsheets")
    python = Topic.objects.create(topic="python programming")
    mortgages = Topic.objects.create(topic="mortgages")
    cocaine = Topic.objects.create(topic="cocaine")
    capitalism = Topic.objects.create(topic="capitalism")
    investment = Topic.objects.create(topic="investment")
    yoga = Topic.objects.create(topic="yoga")
    trainspotting = Topic.objects.create(topic="trainspotting")
    birdwatching = Topic.objects.create(topic="birdwatching")
    tiktok = Topic.objects.create(topic="tiktok dances")

    # create some mentors
    john = User.objects.create(
        first_name="John",
        last_name="Mentor",
        email="john@gmail.com",
        business_area=money_laundering,
        user_type=mentor_type,
    )
    # john is really into his yoga these days
    UserTopic.objects.create(user=john, topic=yoga)

    steve = User.objects.create(
        first_name="Steve",
        last_name="The Banker",
        email="steve@db.com",
        business_area=tax_evasion,
        user_type=mentor_type,
    )
    UserTopic.objects.create(user=steve, topic=python)
    UserTopic.objects.create(user=steve, topic=trainspotting)

    # craig is a very serious banker. John thinks he needs to lighten up a little, its starting to affect their marriage.
    craig = User.objects.create(
        first_name="Craig",
        last_name="Mentor",
        email="craig@db.com",
        business_area=global_economy_manipulation,
        user_type=mentor_type,
    )
    UserTopic.objects.create(user=craig, topic=stonks)
    UserTopic.objects.create(user=craig, topic=spreadsheets)
    UserTopic.objects.create(user=craig, topic=management)

    # james was secretly a db employee all along
    james = User.objects.create(
        first_name="James",
        last_name="Archbold",
        email="james.archbold@warwick.ac.uk",
        business_area=money_laundering,
        user_type=mentor_type,
    )
    UserTopic.objects.create(user=james, topic=making_money)
    UserTopic.objects.create(user=james, topic=capitalism)
    UserTopic.objects.create(user=james, topic=investment)

    # james is a very busy man as he already has three mentees
    # just dummy to fill the database
    james_mentee_1 = User.objects.create(
        first_name="",
        last_name="",
        email="",
        business_area=financing_nonces,
        user_type=mentee_type,
    )
    MentorMentee.objects.create(
        mentor=james,
        mentee=james_mentee_1,
        approved=True,
    )
    james_mentee_2 = User.objects.create(
        first_name="",
        last_name="",
        email="",
        business_area=financing_nonces,
        user_type=mentee_type,
    )
    MentorMentee.objects.create(
        mentor=james,
        mentee=james_mentee_2,
        approved=True,
    )
    james_mentee_3 = User.objects.create(
        first_name="",
        last_name="",
        email="",
        business_area=financing_nonces,
        user_type=mentee_type,
    )
    MentorMentee.objects.create(
        mentor=james,
        mentee=james_mentee_3,
        approved=True,
    )

    # I also work for db. surprise!
    # I am a mentor AND a mentee. interesting.
    joey = User.objects.create(
        first_name="Joey",
        last_name="Harrison",
        email="joey@db.com",
        business_area=tax_evasion,
        user_type=mentor_mentee_type,
    )
    UserTopic.objects.create(
        user=joey, topic=python, usertype=mentor_type
    )  # already an expert in python
    UserTopic.objects.create(
        user=joey, topic=crypto, usertype=mentor_type
    )  # already an expert in python
    UserTopic.objects.create(
        user=joey, topic=tiktok, usertype=mentor_type
    )  # already an expert in python
    UserTopic.objects.create(
        user=joey, topic=trainspotting, usertype=mentee_type
    )  # want to learn about birdwatching, which i am doing from steve

    # I have a mentee, but am under the mentorship of steve
    joeys_mentee = User.objects.create(
        first_name="",
        last_name="",
        email="",
        business_area=financing_nonces,
        user_type=mentee_type,
    )
    MentorMentee.objects.create(
        mentor=joey,
        mentee=joeys_mentee,
        approved=True,
    )
    MentorMentee.objects.create(
        mentor=steve,
        mentee=joey,
        approved=True,
    )

    # also give me an awful review so theres no way i get any new mentees
    # my mentee thinks my tiktok dances are awful
    Rating.objects.create(
        mentor=joey, rating=1, associated_topic=tiktok, rated_by=joeys_mentee
    )
    # create some new mentees
    # these will be our test cases
    tim = User.objects.create(
        first_name="Tim",
        last_name="Mentee",
        email="tim@db.com",
        business_area=money_laundering,
        user_type=mentee_type,
    )
    # tim wants to learn more about python programming and trainspotting
    # maybe steve could help him with this?
    UserTopic.objects.create(user=tim, topic=python)
    UserTopic.objects.create(user=tim, topic=trainspotting)

    # sandra is a new intern working on the epstein account, and wants to upskill herself in modern banking practice
    sandra = User.objects.create(
        first_name="Sandra",
        last_name="The Intern",
        email="sandra@db.com",
        business_area=financing_nonces,
        user_type=mentee_type,
    )
    UserTopic.objects.create(user=sandra, topic=cocaine)
    UserTopic.objects.create(user=sandra, topic=crypto)
    UserTopic.objects.create(user=sandra, topic=tiktok)
    UserTopic.objects.create(user=sandra, topic=yoga)

    alex = User.objects.create(
        first_name="Alex",
        last_name="Ander",
        email="alex@gmail.net",
        business_area=tax_evasion,
        user_type=mentee_type,
    )
    # alex knows he has a lot to learn!
    UserTopic.objects.create(user=alex, topic=making_money)
    UserTopic.objects.create(user=alex, topic=mortgages)
    UserTopic.objects.create(user=alex, topic=capitalism)
    UserTopic.objects.create(user=alex, topic=investment)
    UserTopic.objects.create(user=alex, topic=stonks)
    UserTopic.objects.create(user=alex, topic=spreadsheets)
