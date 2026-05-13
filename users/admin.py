from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from main.models import Doctor, Patient  # импортируем модели врача и пациента


class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Профиль врача'
    fk_name = 'user'
    fields = ('name', 'specialization', 'bio', 'phone', 'email', 'photo',
              'experience', 'degree', 'clinic_address', 'specialization_list')
    extra = 1  # показывать пустую форму для создания профиля врача


class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Профиль пациента'
    fk_name = 'user'
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'full_name', 'phone')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('full_name', 'phone'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('full_name', 'phone', 'email'),
        }),
    )

    inlines = [DoctorInline, PatientInline]