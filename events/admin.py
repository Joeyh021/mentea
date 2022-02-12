from django.contrib import admin

from events.models import Answer, FeedbackForm, FeedbackSubmission, QuestionType, Questions

# Register your models here.

@admin.register(FeedbackForm)
class AdminFeedbackForm(admin.ModelAdmin):
    list_display=('name',)
    pass
@admin.register(FeedbackSubmission)
class AdminFeedbackSubmission(admin.ModelAdmin):
    pass
@admin.register(Questions)
class AdminQuestion(admin.ModelAdmin):
    pass
@admin.register(QuestionType)
class AdminQuestionType(admin.ModelAdmin):
    list_display =('name',)

@admin.register(Answer)
class AdminAnswer(admin.ModelAdmin):
    pass