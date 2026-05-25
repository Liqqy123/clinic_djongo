from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from django.utils.text import slugify

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        null=True, blank=True,
        verbose_name='Пользователь'
    )
    name = models.CharField(max_length=200, verbose_name='Имя')
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Специализация')
    bio = models.TextField(blank=True, verbose_name='Биография')
    phone = models.CharField(max_length=20, blank=True, default='', verbose_name='Телефон')
    email = models.EmailField(blank=True, default='', verbose_name='Email')
    photo = models.ImageField(upload_to='doctors_photos/', blank=True, null=True, verbose_name='Фото')
    experience = models.PositiveIntegerField(blank=True, null=True, verbose_name='Стаж (лет)')
    degree = models.CharField(max_length=200, blank=True, verbose_name='Учёная степень/категория')
    clinic_address = models.CharField(max_length=300, blank=True, verbose_name='Клиника/адрес')
    specialization_list = models.TextField(blank=True, help_text='Специализация (каждый пункт с новой строки)', verbose_name='Специализация (подробно)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['name']

    def __str__(self):
        return self.name

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        null=True, blank=True,
        verbose_name='Пользователь'
    )
    patient_id = models.CharField(max_length=20, unique=True, verbose_name='ID пациента')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        null=True, blank=True,
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