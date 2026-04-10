from django.contrib import admin

# Register your models here.
# admin.py
from .models import Project

admin.site.register(Project)