from django.forms import model_to_dict
from django.http import JsonResponse

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from events.models import Answer, FeedbackForm, FeedbackSubmission, Questions

from django import forms
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse

from django.shortcuts import render
from django.views.generic import TemplateView

from typing import Any


class JsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return model_to_dict(o)
        return super().default(o)


class FormValidator(forms.Form):
    jsonData = forms.JSONField()


class FeedbackFormReturn(TemplateView):
    def get(self, request: HttpRequest, formId=None):
        feedbackForm = get_object_or_404(FeedbackForm, id=formId)
        # feedbackForm = FeedbackForm.objects.get(id=formId)

        # questions = json.loads(serializers.serialize('json', Questions.objects.filter(form=formId)))
        questions = (
            Questions.objects.filter(form=formId).order_by("order").all().values()
        )

        # Gather any previous submissions for the user (if logged in)

        if request.user.is_authenticated:
            responses = (
                FeedbackSubmission.objects.filter(form=feedbackForm, user=request.user)
                .all()
                .values("id")
            )

            return JsonResponse(
                {
                    "formData": feedbackForm,
                    "previousSubmissions": list(responses),
                    "questions": list(questions),
                },
                safe=False,
                encoder=JsonEncoder,
            )
        else:
            return JsonResponse(
                {"formData": feedbackForm, "questions": list(questions)},
                safe=False,
                encoder=JsonEncoder,
            )


class FeedbackFormCreate(TemplateView):
    def post(self, request):
        form = FormValidator(request.POST)
        if form.is_valid():

            data = json.loads(form.data["jsonData"])

            if "name" not in data["formData"] or data["formData"]["name"] == "":
                return HttpResponse("Missing name")

            if "desc" not in data["formData"]:
                return HttpResponse("Missing desc")

            if "questions" not in data or data["questions"] == []:
                return HttpResponse("Missing questions")

            ff = FeedbackForm(
                name=data["formData"]["name"], desc=data["formData"]["desc"]
            )
            ff.save()

            qIds = []

            order = 0
            for q in data["questions"]:
                type_data = ""
                if "type_data" in q:
                    type_data = q["type_data"]
                question = Questions(
                    name=q["name"],
                    type=q["type"],
                    type_data=type_data,
                    required=q["required"],
                    order=order,
                    form=ff,
                )
                question.save()
                qIds.append(question.id)
                order = order + 1

            return JsonResponse(
                {"result": "success", "data": {"formId": ff.id, "questionIds": qIds}}
            )
        else:
            return HttpResponse(form.errors.as_json())


class FeedbackFormEditorEdit(TemplateView):
    def post(self, request):
        form = FormValidator(request.POST)
        if form.is_valid():
            data = json.loads(form.data["jsonData"])

            if "id" not in data["formData"] or data["formData"]["id"] == "":
                return HttpResponse("Missing Form ID")

            if "name" not in data["formData"] or data["formData"]["name"] == "":
                return HttpResponse("Missing name")

            if "desc" not in data["formData"]:
                return HttpResponse("Missing desc")

            if "questions" not in data or data["questions"] == []:
                return HttpResponse("Missing questions")

            formId = data["formData"]["id"]

            try:
                ff = FeedbackForm.objects.get(id=formId)

                ff.name = data["formData"]["name"]
                ff.desc = data["formData"]["desc"]

                ff.save()

                questionsIds = []

                order = 0
                for q in data["questions"]:
                    type_data = ""
                    if "type_data" in q:
                        type_data = q["type_data"]

                    (question, c) = Questions.objects.get_or_create(
                        id=q["id"],
                        defaults={
                            "name": q["name"],
                            "type": q["type"],
                            "type_data": type_data,
                            "required": q["required"],
                            "order": order,
                            "form": ff,
                        },
                    )

                    if not c:
                        question.name = q["name"]
                        question.type = q["type"]
                        question.type_data = type_data
                        question.required = q["required"]
                        question.order = order

                        question.save()
                    questionsIds.append(question.id)
                    order = order + 1

                # DELETE FROM forms WHERE form=? AND id NOT IN (?,?,?)

                toDelete = Questions.objects.filter(form=ff.id).exclude(
                    id__in=questionsIds
                )
                toDelete.delete()

                return JsonResponse({"result": "success", "data": ff.id})

            except Exception as err:
                print(err)

                return HttpResponse("No form found with this given ID")

        else:
            return HttpResponse(form.errors.as_json())


class FeedbackFormSubmissionHandler(TemplateView):
    def get(self, request, submissionId=None):
        submission = get_object_or_404(FeedbackSubmission, id=submissionId)

        answers = (
            Answer.objects.filter(associated_submission=submission)
            .all()
            .values("id", "associated_question", "data")
        )

        return JsonResponse(
            {"submissionData": submission, "answers": list(answers)},
            safe=False,
            encoder=JsonEncoder,
        )

    def post(self, request):
        form = FormValidator(request.POST)
        if form.is_valid():
            data = json.loads(form.data["jsonData"])

            if "formId" not in data or data["formId"] == "":
                return HttpResponse("Missing Form ID")

            if "answers" not in data or data["answers"] == []:
                return HttpResponse("Missing answers")

            formId = data["formId"]

            ff = get_object_or_404(FeedbackForm, id=formId)

            submission = FeedbackSubmission(user=request.user, form=ff)
            submission.save()

            try:
                for a in data["answers"]:
                    quest = Questions.objects.get(id=a["q"])
                    answer = Answer(
                        associated_question=quest,
                        associated_submission=submission,
                        data=a["a"],
                    )
                    answer.save()

            except Exception as err:
                submission.delete()
                return JsonResponse(
                    {
                        "result": "error",
                        "data": "A given question wasn't found in the database, try refreshing the form!",
                    }
                )

            return JsonResponse({"result": "success", "data": submission.id})

        else:
            return HttpResponse(form.errors.as_json())


class FeedbackFormSubmissionUpdateHandler(TemplateView):
    def post(self, request):
        form = FormValidator(request.POST)
        if form.is_valid():
            data = json.loads(form.data["jsonData"])

            if "submissionId" not in data or data["submissionId"] == "":
                return HttpResponse("Missing Submission ID")

            if "answers" not in data or data["answers"] == []:
                return HttpResponse("Missing answers")

            subId = data["submissionId"]

            ss = get_object_or_404(FeedbackSubmission, id=subId)

            try:
                for a in data["answers"]:
                    answer = Answer.objects.get(
                        associated_question=a["q"], associated_submission=ss
                    )
                    answer.data = a["a"]

                    answer.save()

            except Exception as err:

                return JsonResponse(
                    {
                        "result": "error",
                        "data": "Unable to update an answer!",
                    }
                )

            return JsonResponse({"result": "success", "data": ss.id})

        else:
            return HttpResponse(form.errors.as_json())


class FeedbackFormBuilder(TemplateView):
    """contains privacy and GDPR notices. We care about your data:tm:"""

    template_name: str = "main/feedback-builder.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class FeedbackFormSubmissions(TemplateView):
    def get(self, request: HttpRequest, formId=None) -> HttpResponse:
        submissions = FeedbackSubmission.objects.filter(form=formId).all().values("id")
        return JsonResponse(
            {"submissions": list(submissions)},
            safe=False,
            encoder=JsonEncoder,
        )
