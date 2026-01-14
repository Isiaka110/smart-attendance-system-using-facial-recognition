import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Student, Session, Attendance

def seed_data():
    print("🌱 Starting data seeding...")

    # 1. Create Students
    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

    students = []
    for i in range(1, 51):
        s = Student.objects.create(
            student_id=f"2026-ENG-{100 + i}",
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
        )
        students.append(s)
    print(f"✅ Created {len(students)} students.")

    # 2. Create Sessions
    session_names = ["Morning Physics", "Intro to AI", "Data Structures", "Ethics in Tech", "Calculus II"]
    sessions = []
    for name in session_names:
        sess = Session.objects.create(
            name=name,
            start_time=timezone.now() - timedelta(days=random.randint(1, 10)),
            end_time=timezone.now() + timedelta(hours=2),
            is_active=True
        )
        sessions.append(sess)
    print(f"✅ Created {len(sessions)} active sessions.")

    # 3. Create Random Attendance
    # We want some students to have high attendance and some low for the assessment bars
    for student in students:
        # Each student attends a random number of the created sessions
        attended_sessions = random.sample(sessions, random.randint(0, len(sessions)))
        
        for sess in attended_sessions:
            Attendance.objects.create(
                student=student,
                session=sess,
                type='START',
                timestamp=sess.start_time + timedelta(minutes=random.randint(1, 15))
            )
    
    print("🚀 Seeding complete! Go to the Assessment page to see the results.")

if __name__ == "__main__":
    seed_data()