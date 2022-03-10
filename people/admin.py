from django.contrib import admin

from events.models import MeetingRequest

from .models import BusinessArea, MentorMentee, Notification, Topic, User, UserType

# Register your models here.


admin.site.register(User)
admin.site.register(BusinessArea)
admin.site.register(Topic)
admin.site.register(Notification)
admin.site.register(MentorMentee)
admin.site.register(MeetingRequest)
