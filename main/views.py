from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from typing import Any


class IndexPage(TemplateView):
    """the main site homepage: mentea.com or whatever"""

    template_name: str = "main/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class FAQPage(TemplateView):
    """contains FAQs and other support information"""

    template_name: str = "main/faq.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class PrivacyPage(TemplateView):
    """contains privacy and GDPR notices. We care about your data:tm:"""

    template_name: str = "main/privacy.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})


class FeedbackPage(TemplateView):
    """A page with a feedback box allowing users to send feedback about the application.""" ""

    template_name: str = "main/feedback.html"

    def get(self, request: HttpRequest, *args: Any, **kwarsgs: Any) -> HttpResponse:
        return render(request, self.template_name, {})
