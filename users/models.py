from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('patient', 'Пациент'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient', verbose_name='Роль')
    phone = models.CharField(max_length=16, unique=True, verbose_name='Телефон')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def full_name(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'