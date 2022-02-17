from django.contrib import admin
import django_stubs_ext

django_stubs_ext.monkeypatch()

from .models import *

# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin[User]):
    pass
