from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=16, unique=True, verbose_name='Телефон')
    email = models.EmailField(unique=True, verbose_name='Email')

    def __str__(self):
        return self.username

    def get_role(self):
        if self.is_superuser:
            return 'Администратор'
        if hasattr(self, 'doctor_profile'):
            return 'Врач'
        if hasattr(self, 'patient_profile'):
            return 'Пациент'
        return 'Пользователь'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'