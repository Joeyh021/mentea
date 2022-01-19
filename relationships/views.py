from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class RelationshipsIndexPage(TemplateView):
    template_name = "relationships/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
