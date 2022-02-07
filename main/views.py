from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPage(TemplateView):
    """the main site homepage: mentea.com or whatever"""

    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class FAQPage(TemplateView):
    """contains FAQs and other support information"""

    template_name = "main/faq.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class PrivacyPage(TemplateView):
    """contains privacy and GDPR notices. We care about your data:tm:"""

    template_name = "main/privacy.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class FeedbackPage(TemplateView):
    """A page with a feedback box allowing users to send feedback about the application.""" ""

    template_name = "main/feedback.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
