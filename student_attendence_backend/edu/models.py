from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils.timezone import now

User = get_user_model()

# Student Profile Model
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    contact_details = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.full_name} ({self.roll_no})"

# Teacher Profile Model
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)  # Unique ID for teachers
    contact_details = models.CharField(max_length=15)
    address = models.TextField()
    subjects_taught = models.ManyToManyField('Subject', related_name="teachers")  # Teachers can teach multiple subjects

    def __str__(self):
        return f"{self.user.full_name} ({self.employee_id})"

# Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    total_hours = models.IntegerField()  # Fixed total hours for attendance percentage

    def __str__(self):
        return self.name

# Schedule Model (For Classes)
class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)  # Assign a teacher
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(
        max_length=10,
        choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                 ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')]
    )

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.user.full_name} - {self.day_of_week} ({self.start_time} - {self.end_time})"

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    hours_attended = models.FloatField(default=0)  # Hours attended in a session
    is_present = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.student.user.full_name} - {self.subject.name} - {self.date}"

    def calculate_attendance_percentage(self):
        total_subject_hours = self.subject.total_hours
        if total_subject_hours > 0:
            return (self.hours_attended / total_subject_hours) * 100
        return 0

# Attendance Summary Manager
class AttendanceSummaryManager(models.Manager):
    def get_monthly_attendance(self, student, month=None, year=None):
        if month is None or year is None:
            today = now().date()
            month, year = today.month, today.year
        
        attendance_data = Attendance.objects.filter(
            student=student,
            date__year=year,
            date__month=month
        ).values('subject__name').annotate(total_hours=Sum('hours_attended'))
        
        return {entry['subject__name']: entry['total_hours'] for entry in attendance_data}

def create_sample_entries():
    from django.contrib.auth import get_user_model
    from edu.models import TeacherProfile, Subject, Schedule, Attendance

    User = get_user_model()

    # Get the existing user for the teacher
    teacher_user = User.objects.get(email='ashmascarenhas5@gmail.com')

    # Check if a teacher profile already exists
    if not TeacherProfile.objects.filter(user=teacher_user).exists():
        # Create a teacher profile
        teacher_profile = TeacherProfile.objects.create(
            user=teacher_user,
            employee_id='EMP001',
            contact_details='1234567890',
            address='123 Teacher St, Education City'
        )

        # Create a subject
        subject = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
            total_hours=40
        )

        # Assign the subject to the teacher
        teacher_profile.subjects_taught.add(subject)

        # Create a schedule for the subject
        schedule = Schedule.objects.create(
            subject=subject,
            teacher=teacher_profile,
            start_time='09:00:00',
            end_time='10:00:00',
            day_of_week='Monday'
        )

        # Create attendance entries
        attendance_entry = Attendance.objects.create(
            student=student_profile,  # Assuming student_profile is already created
            subject=subject,
            hours_attended=1,
            is_present=True
        )
