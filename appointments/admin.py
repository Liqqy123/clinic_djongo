from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('user__username', 'user__email', 'doctor__name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Информация о записи', {
            'fields': ('user', 'doctor', 'date', 'time', 'notes')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )