from django.contrib import admin
from .models import Doctor, DoctorSchedule, Appointment, MedicalRecord, Payment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'get_user', 'user')
    search_fields = ('name', 'specialization', 'user__username')
    list_filter = ('specialization',)
    fieldsets = (
        ('Учетная запись', {
            'fields': ('user',),
            'description': 'Привяжите существующего пользователя или оставьте пусто, если врач не будет входить в систему',
        }),
        ('Информация о враче', {
            'fields': ('name', 'specialization', 'bio'),
        }),
    )

    def get_user(self, obj):
        return obj.user.get_full_name() if obj.user else '—'
    get_user.short_description = 'Пользователь'


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'doctor')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'doctor', 'date')
    search_fields = ('patient_name', 'notes')
    readonly_fields = ('created_at',)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'created_at')
    search_fields = ('patient_name', 'description')
    list_filter = ('doctor', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'method', 'paid_at')
    list_filter = ('method', 'paid_at')
    readonly_fields = ('paid_at',)