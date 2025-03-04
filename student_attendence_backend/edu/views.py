from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Attendance, Subject, StudentProfile, User
from django.shortcuts import render
from django.db.models import Sum
from .models import TeacherProfile, Attendance, Subject
from django.core import serializers
import json



@login_required
def student_dashboard(request):
    # Get the logged-in student's profile
    student = StudentProfile.objects.get(user=request.user)

    # Get all attendance records for the student (not limited to the current month)
    attendance_data = Attendance.objects.filter(student=student).values('subject__id', 'subject__name').annotate(
        total_hours=Sum('hours_attended')
    )

    labels = []
    data = []  # Total hours attended
    percentages = []  # Attendance percentage
    total_percentage = 0  # For cumulative attendance
    subject_count = 0  # To calculate average

    for entry in attendance_data:
        subject_id = entry['subject__id']
        subject_name = entry['subject__name']
        total_hours_attended = entry['total_hours']

        # Get total required hours for the subject from Subject model
        subject = Subject.objects.get(id=subject_id)
        total_subject_hours = subject.total_hours  # Fixed total hours

        # Calculate attendance percentage per subject
        if total_subject_hours > 0:
            attendance_percentage = (total_hours_attended / total_subject_hours) * 100
            total_percentage += attendance_percentage
            subject_count += 1
        else:
            attendance_percentage = 0

        # Append data for frontend charts
        labels.append(subject_name)
        data.append(total_hours_attended)
        percentages.append(round(attendance_percentage, 2))  # Round to 2 decimal places

    # Calculate the overall average attendance percentage
    avg_attendance_percentage = round(total_percentage / subject_count, 2) if subject_count > 0 else 0

    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'percentages': json.dumps(percentages),
        'avg_attendance_percentage': float(avg_attendance_percentage),
        'user_profession': request.user.profession.title(),  # Add this
        'user_name': request.user.full_name  # Add this
    }
    return render(request, 'edu/stu_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    try:
        # Get the logged-in teacher's profile
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        messages.error(request, "Teacher profile does not exist.")
        return redirect("edu:teacher_dashboard")  # Redirect to a suitable page
    
    # Get subjects taught by the teacher
    subjects = Subject.objects.filter(teachers=teacher)
    
    labels = []
    data = []
    percentages = []
    total_percentage = 0
    subject_count = 0

    for subject in subjects:
        # Get total hours attended by students in this subject
        total_hours_attended = Attendance.objects.filter(subject=subject).aggregate(
            Sum('hours_attended'))['hours_attended__sum'] or 0
        total_subject_hours = subject.total_hours

        # Calculate attendance percentage
        if total_subject_hours > 0:
            attendance_percentage = (total_hours_attended / total_subject_hours) * 100
            total_percentage += attendance_percentage
            subject_count += 1
        else:
            attendance_percentage = 0

        labels.append(subject.name)
        data.append(total_hours_attended)
        percentages.append(round(attendance_percentage, 2))

    # Calculate average attendance
    avg_attendance_percentage = round(total_percentage / subject_count, 2) if subject_count > 0 else 0

    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'percentages': json.dumps(percentages),
        'avg_attendance_percentage': avg_attendance_percentage,
        'user_profession': request.user.profession.title(),  # Add this
        'user_name': request.user.full_name  # Add this
    }
    
    return render(request, "edu/tchr_dashboard.html", context)


@login_required
def stu_add(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        roll_no = request.POST.get("roll_no")
        date_of_birth = request.POST.get("date_of_birth")  # Format: YYYY-MM-DD
        email = request.POST.get("email")
        contact_details = request.POST.get("contact_details")
        address = request.POST.get("address")

        # Ensure all fields are provided
        if not all([full_name, roll_no, date_of_birth, email, contact_details, address]):
            messages.error(request, "All fields are required.")
            return redirect("stu_add")

        # Generate default password: roll number + birth year
        birth_year = date_of_birth.split("-")[0]  # Extract year from YYYY-MM-DD
        default_password = f"{roll_no}{birth_year}"

        # Create the user (CustomUser)
        user = User.objects.create_user(
            email=email,
            password=default_password,
            full_name=full_name,
            profession="student"
        )

        # Create the StudentProfile
        StudentProfile.objects.create(
            user=user,
            roll_no=roll_no,
            date_of_birth=date_of_birth,
            contact_details=contact_details,
            address=address
        )

        messages.success(request, "Student registered successfully! The default password is their Roll Number + Birth Year.")
        return redirect("edu:teacher_dashboard")  # Redirect to the form page after submission

    return render(request, "edu/new_stu_details.html")

@login_required
def stu_details(request):
    return render(request, "edu/stu_details.html")
