from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class PeopleIndexView(TemplateView):
    template_name = "people/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
