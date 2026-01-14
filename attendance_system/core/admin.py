# core/admin.py
from django.contrib import admin
from .models import Student, Attendance, Session

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Session)