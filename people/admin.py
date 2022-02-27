from django.contrib import admin

from .models import BusinessArea, Topic, User, UserType

# Register your models here.


admin.site.register(User)
admin.site.register(BusinessArea)
admin.site.register(Topic)
