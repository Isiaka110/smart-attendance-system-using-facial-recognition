from django.db import models
from django.utils import timezone

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    # The photo that will be used to train the recognizer for this student
    photo = models.ImageField(upload_to='students/') 

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def calculate_attendance_points(self, max_points=10):
        """Calculates points based on sessions attended vs total sessions."""
        total_sessions = Session.objects.filter(is_active=True).count()
        if total_sessions == 0:
            return 0
        
        # Count how many sessions this student has a 'START' record for
        attended_count = Attendance.objects.filter(
            student=self, 
            type='START'
        ).values('session').distinct().count()

        attendance_percentage = (attended_count / total_sessions)
        return round(attendance_percentage * max_points, 1)



class Session(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class Attendance(models.Model):
    ATTENDANCE_TYPES = [('START', 'Start'), ('FINISH', 'Finish')]
    
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ATTENDANCE_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents duplicate start/finish for the same session
        unique_together = ['student', 'session', 'type']