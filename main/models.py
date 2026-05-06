from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_profile')
    name = models.CharField('ФИО', max_length=120)
    specialization = models.CharField('Специальность', max_length=120)
    bio = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} — {self.specialization}'


class DoctorSchedule(models.Model):
    DAY_CHOICES = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.PositiveSmallIntegerField('День недели', choices=DAY_CHOICES)
    start_time = models.TimeField('Начало приема')
    end_time = models.TimeField('Конец приема')

    class Meta:
        verbose_name = 'График врача'
        verbose_name_plural = 'Графики врачей'
        ordering = ['doctor', 'day_of_week', 'start_time']

    def __str__(self):
        return f'{self.doctor.name}: {self.get_day_of_week_display()} {self.start_time}–{self.end_time}'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    patient_name = models.CharField('Пациент', max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments')
    date = models.DateField('Дата приема')
    time = models.TimeField('Время приема')
    notes = models.TextField('Причина обращения', blank=True)
    status = models.CharField('Статус', max_length=16, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Дата записи', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-date', 'time']

    def __str__(self):
        return f'{self.patient_name} — {self.doctor.name} ({self.date} {self.time})'


class MedicalRecord(models.Model):
    patient_name = models.CharField('Пациент', max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='medical_records')
    description = models.TextField('Медицинская карта')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Медицинская карта'
        verbose_name_plural = 'Медицинские карты'
        ordering = ['-created_at']

    def __str__(self):
        return f'Карточка {self.patient_name} — {self.created_at.date()}'


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Карта'),
        ('cash', 'Наличные'),
        ('online', 'Онлайн'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField('Сумма', max_digits=9, decimal_places=2)
    method = models.CharField('Метод оплаты', max_length=16, choices=PAYMENT_METHODS)
    paid_at = models.DateTimeField('Дата оплаты', auto_now_add=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-paid_at']

    def __str__(self):
        return f'{self.amount} ₽ — {self.appointment.patient_name}'
