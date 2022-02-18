import json
from django import forms
from django.forms import model_to_dict
from django.http import JsonResponse
from django.template import RequestContext
from django.urls import path, include

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from events.models import FeedbackForm, Questions

from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = "main"

class JsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return model_to_dict(o)
        return super().default(o)
    
class FormValidator(forms.Form):
    jsonData = forms.JSONField()

class FeedbackFormReturn(TemplateView):
    def get(self, request: HttpRequest, formId=None):
        feedbackForm = FeedbackForm.objects.get(id=formId)
        
        questions = json.loads(serializers.serialize('json', Questions.objects.filter(form=formId)))
  
        return JsonResponse({'formData': feedbackForm, 'questions': questions}, safe = False, encoder=JsonEncoder)
    
    def post(self, request, formId):
        form = FormValidator(request.POST)
        if form.is_valid():
            
            data = json.loads(form.data['jsonData'])
            
            ff = FeedbackForm(name= data['formData']['name'], desc = data['formData']['desc'])
            ff.save()
            
            return HttpResponse(ff.id)
        else:
            return HttpResponse(form.errors.as_json())
    

        



urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("faq/", FAQPage.as_view(), name="faq"),
    path("privacy/", PrivacyPage.as_view(), name="privacy"),
    path("feedback/", FeedbackPage.as_view(), name="feedback"),
    path("terms-of-service/", TermosOfServicePage.as_view(), name="tos"),
    path("feedback-api/<uuid:formId>/",csrf_exempt( FeedbackFormReturn.as_view()), name="ff-get"),
]
