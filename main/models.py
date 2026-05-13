from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    name = models.CharField(max_length=200, verbose_name='Имя')
    specialization = models.CharField(max_length=200, verbose_name='Специализация')
    phone = models.CharField(max_length=20, blank=True, default='', verbose_name='Телефон')
    email = models.EmailField(blank=True, default='', verbose_name='Email')
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(
        upload_to='doctors_photos/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    experience = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Стаж (лет)'
    )
    degree = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Учёная степень/категория'
    )
    clinic_address = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Клиника/адрес'
    )
    specialization_list = models.TextField(
        blank=True,
        help_text='Специализация (каждый пункт с новой строки)',
        verbose_name='Специализация (подробно)'
    )

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return f"{self.name} ({self.specialization})"

class Schedule(models.Model):
    DAYS = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
    ]
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Врач'
    )
    day_of_week = models.CharField(max_length=20, choices=DAYS, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Начало работы')
    end_time = models.TimeField(verbose_name='Конец работы')

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'

    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_of_week_display()}"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    patient_id = models.CharField(max_length=20, unique=True, verbose_name='ID пациента')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        null=True,
        blank=True,
        verbose_name='Возраст'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Пол')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Адрес')
    allergies = models.TextField(blank=True, help_text="Известные аллергии", verbose_name='Аллергии')
    medical_history = models.TextField(
        blank=True,
        help_text="Медицинская история, текущие лекарства",
        verbose_name='Медицинская история'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def prescription_count(self):
        return self.prescriptions.count()


class Prescription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    prescription_id = models.CharField(max_length=20, unique=True, verbose_name='ID рецепта')
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Пациент'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prescriptions',
        verbose_name='Врач'
    )
    diagnosis = models.TextField(verbose_name='Диагноз')
    medications = models.TextField(help_text="Список лекарств с дозировкой", verbose_name='Лекарства')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    issue_date = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f"{self.prescription_id} - {self.patient.full_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    patient_name = models.CharField(max_length=200, verbose_name='Имя пациента')
    patient_phone = models.CharField(max_length=20, verbose_name='Телефон пациента')
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
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

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} - {self.date}"


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Ожидает'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка'),
    ]

    patient_name = models.CharField(max_length=200, verbose_name='Имя пациента')
    patient_phone = models.CharField(max_length=20, verbose_name='Телефон пациента')
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Врач'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    purpose = models.CharField(max_length=200, help_text="Назначение платежа", verbose_name='Назначение')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"{self.patient_name} - {self.amount} руб."