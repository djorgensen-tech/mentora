from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Textbook


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('username', 'first_name', 'email', 'grade_level', 'is_staff', 'date_joined')
    list_filter   = ('grade_level', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'email')
    ordering      = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Mentora', {'fields': ('grade_level',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Mentora', {'fields': ('first_name', 'email', 'grade_level')}),
    )