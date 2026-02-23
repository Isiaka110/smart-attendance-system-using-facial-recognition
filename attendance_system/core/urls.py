from django.urls import path
from . import views

urlpatterns = [
    # The empty path is your Landing Page
    path('', views.landing_page, name='landing'),

    # THIS IS THE MISSING LINE:
    path('dashboard/', views.index, name='index'),

    # ... keep your other paths below ...
    path('video_feed/', views.video_feed, name='video_feed'),
    path('attendance-api/', views.attendance_list_api, name='attendance_api'),
    path('register/', views.register_student, name='register'),
    path('confirm-registration/', views.confirm_registration, name='confirm_registration'),
    path('export-csv/', views.export_attendance_csv, name='export_csv'),
    path('history/', views.attendance_history, name='history'),
    path('assessment/', views.assessment_report, name='assessment_report'),
    path('close-session/<int:session_id>/', views.close_session, name='close_session'),
]