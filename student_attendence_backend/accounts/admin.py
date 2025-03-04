from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser  # Import your custom user model

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the Django admin panel
    list_display = ('email', 'full_name', 'profession', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'profession')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
    (_("Personal Info"), {"fields": ("email", "full_name", "profession", "password")}),
    (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    (_("Important Dates"), {"fields": ("last_login",)}),  
    )


    add_fieldsets = (
        (_("Create User"), {
            "classes": ("wide",),
            "fields": ("email", "full_name", "profession", "password1", "password2"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
