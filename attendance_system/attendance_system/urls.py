"""
URL configuration for attendance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# attendance_system/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views # Import our views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('attendance-api/', views.attendance_list_api, name='attendance_api'), # New URL
    path('export-csv/', views.export_attendance_csv, name='export_csv'), # New URL
    path('register/', views.register_student, name='register'),
path('confirm-registration/', views.confirm_registration, name='confirm_registration'),
path('history/', views.attendance_history, name='history'),
path('assessment/', views.assessment_report, name='assessment_report'),
path('close-session/<int:session_id>/', views.close_session, name='close_session'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)