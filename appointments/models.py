from django.db import models

from django.db import models
from django.conf import settings
from main.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Пациент'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointment_records',  # уникальное related_name, чтобы не конфликтовать с main.Appointment
        verbose_name='Врач'
    )
    date = models.DateField(verbose_name='Дата приёма')
    time = models.TimeField(verbose_name='Время приёма')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Запись на приём'
        verbose_name_plural = 'Записи на приём'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} -> {self.doctor.name} ({self.date})"