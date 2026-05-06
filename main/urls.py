from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='clinic_home'),
    path('register/', views.register, name='clinic_register'),
    path('login/', views.patient_login, name='clinic_login'),
    path('logout/', views.patient_logout, name='clinic_logout'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointment/<int:appointment_id>/status/<str:status>/', views.doctor_update_appointment_status, name='doctor_update_appointment_status'),
    path('doctors/', views.doctor_list, name='clinic_doctors'),
    path('appointments/', views.book_appointment, name='clinic_appointments'),
    path('records/', views.medical_records, name='clinic_records'),
    path('payments/', views.payments, name='clinic_payments'),
]
