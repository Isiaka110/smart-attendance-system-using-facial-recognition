import cv2
import numpy as np
import os
import csv
import base64
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from .models import Student, Attendance, Session
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

# Initialize OpenCV components
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def train_recognizer():
    """Loads student data and trains the recognizer in memory."""
    students = Student.objects.all()
    faces, ids, id_map = [], [], {}

    for student in students:
        if not student.photo: continue
        try:
            img = cv2.imread(student.photo.path)
            if img is None: continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected_faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in detected_faces:
                faces.append(gray[y:y+h, x:x+w])
                ids.append(student.id)
                id_map[student.id] = student
        except: continue

    if len(faces) > 0:
        recognizer.train(faces, np.array(ids))
    return id_map

def gen_frames():
    id_map = train_recognizer()
    video_capture = cv2.VideoCapture(0)

    while True:
        success, frame = video_capture.read()
        if not success: break
        
        now = timezone.now()
        # Find the currently active session (prioritizing the most recently started)
        active_session = Session.objects.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gte=now
        ).order_by('-start_time').first()

        if active_session:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                id_num, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                name = "Unknown"

                if confidence < 80: 
                    student = id_map.get(id_num)
                    if student:
                        name = student.first_name
                        # Attendance Logic
                        start_rec = Attendance.objects.filter(
                            student=student, session=active_session, type='START'
                        ).first()

                        if not start_rec:
                            Attendance.objects.create(student=student, session=active_session, type='START')
                        else:
                            time_diff = now - start_rec.timestamp
                            if time_diff >= timedelta(minutes=7):
                                Attendance.objects.get_or_create(student=student, session=active_session, type='FINISH')

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "NO ACTIVE SESSION", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@login_required
def index(request):
    active_sessions = Session.objects.filter(is_active=True).order_by('-start_time')
    return render(request, 'core/index.html', {'active_sessions': active_sessions})

@login_required
def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def attendance_list_api(request):
    session_id = request.GET.get('session_id')
    try:
        if session_id and session_id != "undefined":
            current_session = Session.objects.get(id=session_id)
        else:
            current_session = Session.objects.filter(is_active=True).latest('start_time')
        
        attendance_query = Attendance.objects.filter(session=current_session).order_by('-timestamp')
        data = {
            "session_name": current_session.name,
            "attendees": [{"id": a.student.student_id, "name": f"{a.student.first_name} {a.student.last_name}", 
                           "type": a.type, "time": a.timestamp.strftime('%H:%M:%S')} for a in attendance_query]
        }
    except:
        data = {"session_name": "No Active Session", "attendees": []}
    return JsonResponse(data)

@login_required
def close_session(request, session_id):
    if request.method == 'POST':
        session = Session.objects.filter(id=session_id).first()
        if session:
            session.is_active = False
            session.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def export_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Session', 'Type', 'Time'])
    for r in Attendance.objects.all().select_related('student', 'session'):
        writer.writerow([r.student.student_id, f"{r.student.first_name} {r.student.last_name}", r.session.name, r.type, r.timestamp])
    return response

@login_required
def confirm_registration(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        format, imgstr = image_data.split(';base64,')
        photo_file = ContentFile(base64.b64decode(imgstr), name=f"{request.POST.get('student_id')}.jpg")
        Student.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            student_id=request.POST.get('student_id'),
            photo=photo_file
        )
        train_recognizer()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def assessment_report(request):
    students = Student.objects.all()
    report_data = [{'student': s, 'points': s.calculate_attendance_points(10), 
                    'status': 'Excellent' if s.calculate_attendance_points(10) > 8 else 'Average' if s.calculate_attendance_points(10) > 5 else 'Low'} 
                   for s in students]
    return render(request, 'core/assessment.html', {'report_data': report_data, 'total_classes': Session.objects.count()})

@login_required
def register_student(request): return render(request, 'core/register.html')

@login_required
def attendance_history(request): return render(request, 'core/history.html', {'history': Attendance.objects.order_by('-timestamp')})