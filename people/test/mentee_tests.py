from django.test.client import Client
from pytest_django import asserts
import pytest

from people.models import PlanOfAction, PlanOfActionTarget

pytestmark = pytest.mark.django_db()


def test_mentee_dashboard_page(client: Client, mentee) -> None:
    response = client.get("/mentee/")
    asserts.assertTemplateUsed(response, "people/mentee_dashboard.html")


def test_plans(client: Client, mentee):
    response = client.get("/mentee/plans/")
    asserts.assertTemplateUsed(response, "people/plans.html")
    # test that the plan from our test data is here
    plan = PlanOfAction.objects.get(associated_mentee=mentee)
    plan_targets = PlanOfActionTarget.objects.filter(associated_poa=plan)
    assert response.context["plans_list"] == [
        {
            "name": "test plan",
            "targets": list(plan_targets),
            "progress": str(plan.progress),
        }
    ]


def test_new_plans(client: Client, mentee):
    response = client.get("/mentee/plans/new/")
    asserts.assertTemplateUsed(response, "people/new_plan.html")
