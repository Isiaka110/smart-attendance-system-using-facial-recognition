"""
URL configuration for attendance_system project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Import our views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Project Landing Page (The first thing users see)
    path('', views.landing_page, name='landing'),

    # Main Attendance Dashboard (Moved from '' to 'dashboard/')
    path('dashboard/', views.index, name='index'),

    # Video/Camera Stream
    path('video_feed/', views.video_feed, name='video_feed'),

    # API and Data Endpoints
    path('attendance-api/', views.attendance_list_api, name='attendance_api'),
    path('export-csv/', views.export_attendance_csv, name='export_csv'),
    path('close-session/<int:session_id>/', views.close_session, name='close_session'),

    # Student Management
    path('register/', views.register_student, name='register'),
    path('confirm-registration/', views.confirm_registration, name='confirm_registration'),

    # Reports and History
    path('history/', views.attendance_history, name='history'),
    path('assessment/', views.assessment_report, name='assessment_report'),
]

# Serving Media Files (Student Photos) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)