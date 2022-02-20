import json
from django import forms
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import path, include

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from events.models import FeedbackForm, Questions

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

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
        feedbackForm = get_object_or_404(FeedbackForm, id=formId)
        #feedbackForm = FeedbackForm.objects.get(id=formId)
        
        
        #questions = json.loads(serializers.serialize('json', Questions.objects.filter(form=formId)))
        questions = Questions.objects.filter(form=formId).order_by('order').all().values()
  
        return JsonResponse({'formData': feedbackForm, 'questions': list(questions)}, safe = False, encoder=JsonEncoder)
    

    
class FeedbackFormCreate(TemplateView):
    def post(self, request):
        form = FormValidator(request.POST)
        if form.is_valid():
            
            data = json.loads(form.data['jsonData'])
            
            if ("name" not in data['formData'] or data['formData']['name'] == ""):
                return HttpResponse('Missing name')
            
            
            if ('desc' not in data['formData']):
                return HttpResponse('Missing desc')
            
            if ('questions' not in data or data['questions'] == []):
                return HttpResponse('Missing questions')
            
            
           
            
            ff = FeedbackForm(name= data['formData']['name'], desc = data['formData']['desc'])
            ff.save()
            
            qIds = []
            
            order = 0
            for q in data['questions']:
                type_data = ""
                if ("type_data" in q):
                    type_data = q['type_data']
                question = Questions(name=q['name'], type=q['type'], type_data=type_data, required=q['required'], order=order, form=ff)
                question.save()
                qIds.append(question.id)
                order = order + 1
                
            
            return JsonResponse({'result': 'success', 'data': {'formId': ff.id, 'questionIds': qIds}})
        else:
            return HttpResponse(form.errors.as_json())
        

            
class FeedbackFormEditorEdit(TemplateView):
    def post(self, request):
        form = FormValidator(request.POST) 
        if form.is_valid():
            data = json.loads(form.data['jsonData'])
            
            if ("id" not in data['formData'] or data['formData']['id'] == ""):
                return HttpResponse('Missing Form ID')
            
            if ("name" not in data['formData'] or data['formData']['name'] == ""):
                return HttpResponse('Missing name')
            
            if ('desc' not in data['formData']):
                return HttpResponse('Missing desc')
            
            if ('questions' not in data or data['questions'] == []):
                return HttpResponse('Missing questions') 
            
            formId = data['formData']['id']
            
            try:
                ff = FeedbackForm.objects.get(id=formId)
                

                
                ff.name = data['formData']['name']
                ff.desc = data['formData']['desc']
                
                ff.save()
                
                questionsIds = []
                
                order = 0
                for q in data['questions']:
                    type_data = ""
                    if ("type_data" in q):
                        type_data = q['type_data']
                        
                        
                    (question, c) = Questions.objects.get_or_create(id=q['id'], defaults={"name": q['name'], 'type':q['type'], 'type_data':type_data, 'required': q['required'], 'order':order, 'form':ff})
                    
                    if (not c):
                        question.name = q['name']
                        question.type = q['type']
                        question.type_data = type_data
                        question.required = q['required']
                        question.order = order
                    
                    
                    
                        question.save()
                    questionsIds.append(question.id)
                    order = order + 1
                    
                # DELETE FROM forms WHERE form=? AND id NOT IN (?,?,?)
                
                toDelete = Questions.objects.filter(form=ff.id).exclude(id__in=questionsIds)
                toDelete.delete()
                
                    
                return JsonResponse({'result': 'success', 'data': ff.id})
                
                
            except Exception as err:
                print(err)
                
                return HttpResponse('No form found with this given ID')
            

            
        else:
            return HttpResponse(form.errors.as_json())

        



urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("faq/", FAQPage.as_view(), name="faq"),
    path("privacy/", PrivacyPage.as_view(), name="privacy"),
    path("feedback/", FeedbackPage.as_view(), name="feedback"),
    path("terms-of-service/", TermosOfServicePage.as_view(), name="tos"),
    path("feedback-api/<uuid:formId>/",csrf_exempt( FeedbackFormReturn.as_view()), name="ff-get"),
    path("feedback-api/create/",csrf_exempt( FeedbackFormCreate.as_view()), name="ff-create"),
    path("feedback-api/editor-edit/",csrf_exempt( FeedbackFormEditorEdit.as_view()), name="ff-editor-edit"),
]
