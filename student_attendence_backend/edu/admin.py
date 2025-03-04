from django.contrib import admin
from django.apps import apps
from django.contrib import admin
from django.db.models import Sum
from django.utils.timezone import now
from .models import StudentProfile, Attendance

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'monthly_attendance_summary')

    def monthly_attendance_summary(self, obj):
        """
        Compute total hours attended per subject dynamically for the current month.
        """
        today = now().date()
        month, year = today.month, today.year

        attendance_data = Attendance.objects.filter(
            student=obj,
            date__year=year,
            date__month=month
        ).values('subject__name').annotate(total_hours=Sum('hours_attended'))

        # Format as a readable string
        summary = ", ".join([f"{entry['subject__name']}: {entry['total_hours']} hrs" for entry in attendance_data])
        return summary if summary else "No records"

    monthly_attendance_summary.short_description = "Monthly Attendance Summary"

# Register the admin
admin.site.register(StudentProfile, StudentProfileAdmin)
# Get all models from the 'edu' app
models = apps.get_app_config('edu').get_models()

# Register each model
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass  # Skip already registered models
