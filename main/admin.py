from django.contrib import admin
from .models import Doctor, Schedule, Patient, Prescription, Appointment, Payment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience', 'degree')
    search_fields = ('name', 'specialization')
    list_filter = ('specialization',)
    fieldsets = (
        (None, {
            'fields': ('name', 'specialization', 'bio', 'photo', 'experience', 'degree', 'clinic_address', 'specialization_list')
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['doctor', 'day_of_week']
    search_fields = ['doctor__name']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'first_name', 'last_name', 'age', 'phone', 'is_active']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone']
    list_filter = ['is_active', 'gender']
    readonly_fields = ['created_at']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_id', 'patient', 'doctor', 'issue_date', 'status']
    search_fields = ['prescription_id', 'patient__first_name', 'patient__last_name']
    list_filter = ['status', 'issue_date']
    readonly_fields = ['issue_date']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'date', 'time', 'status']
    search_fields = ['patient_name', 'patient_phone']
    list_filter = ['status', 'date', 'doctor']
    readonly_fields = ['created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'amount', 'status', 'created_at']
    search_fields = ['patient_name', 'patient_phone']
    list_filter = ['status', 'created_at']