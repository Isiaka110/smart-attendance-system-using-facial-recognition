import datetime
from .models import Session, Attendance, Student

def recognize_face(student_id):
    # 1. Dynamically find the currently active session
    # This ensures that if you switch sessions, the log follows the new one
    current_time = datetime.datetime.now()
    active_session = Session.objects.filter(
        is_active=True, 
        start_time__lte=current_time, 
        end_time__gte=current_time
    ).first()

    if not active_session:
        print("No active session found for this time.")
        return

    # 2. Check if student exists
    student = Student.objects.filter(student_id=student_id).first()
    
    if student:
        # 3. Check for existing attendance in THIS specific session
        # This prevents the "7-minute rule" or "already signed in" logic 
        # from blocking a NEW session.
        last_attendance = Attendance.objects.filter(
            student=student, 
            session=active_session
        ).order_by('-timestamp').first()

        # Logic to create new attendance...
        if not last_attendance:
             Attendance.objects.create(
                 student=student, 
                 session=active_session, 
                 type='START'
             )