from django.test.client import Client
from pytest_django import asserts
import pytest
from people.models import PlanOfAction, PlanOfActionTarget

pytestmark = pytest.mark.django_db()


def test_plans(client: Client, mentee):
    """test the plans of action page works with the data already existing"""
    response = client.get("/mentee/plans/")
    asserts.assertTemplateUsed(response, "people/plans.html")
    # test that the plan from our test data is here
    plan = PlanOfAction.objects.get(associated_mentee=mentee, name="test plan")
    plan_targets = PlanOfActionTarget.objects.filter(associated_poa=plan)
    plans_list = response.context["plans_list"]
    assert plans_list == [
        {
            "name": "test plan",
            "targets": list(plan_targets),
            "progress": str(plan.progress),
        }
    ]
    assert plans_list[0]["targets"][0].description == "sit and write tests all day"
    assert plans_list[0]["progress"] == "50"


def test_new_plans_page(client: Client, mentee):
    """test the new plans page loads"""
    response = client.get("/mentee/plans/new/")
    asserts.assertTemplateUsed(response, "people/new_plan.html")


def test_new_plans_form(client: Client, mentee):
    """test we can submit new plans"""
    # post a new plan
    data = {
        "name": "test plan 2",
        "target_1": "hopefully this test passes",
        "description_1": "",
    }
    response = client.post("/mentee/plans/new/", data=data)
    assert response.status_code == 302

    # check it exists
    response = client.get("/mentee/plans/")
    plan = PlanOfAction.objects.get(associated_mentee=mentee, name="test plan 2")
    plan_targets = PlanOfActionTarget.objects.filter(associated_poa=plan)
    plans_list = response.context["plans_list"]
    assert {
        "name": "test plan 2",
        "targets": list(plan_targets),
        "progress": str(plan.progress),
    } in plans_list

    assert plans_list[1]["targets"][0].name == "hopefully this test passes"
    assert plans_list[1]["progress"] == "0"


def test_complete_target(client: Client, mentee):
    """test we can tick off plans"""
    response = client.post("/mentee/plans/", data={"completed": "run the tests"})
    assert response.status_code == 302  # redirected
    target = PlanOfActionTarget.objects.get(name="run the tests")
    assert target.achieved == True
