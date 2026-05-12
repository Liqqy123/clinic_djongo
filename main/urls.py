from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctor/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('clinics/', views.clinics, name='clinics'),
    path('promotions/', views.promotions, name='promotions'),
    path('services/', views.services, name='services'),

    # Аутентификация
    path('login/', views.clinic_login_view, name='clinic_login'),
    path('register/', views.clinic_register, name='clinic_register'),
    path('logout/', views.clinic_logout_view, name='clinic_logout'),
]