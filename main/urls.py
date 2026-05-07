from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.clinic_home, name='clinic_home'),
    path('doctors/', views.clinic_doctors, name='clinic_doctors'),
    path('appointments/', views.clinic_appointments, name='clinic_appointments'),
    path('records/', views.clinic_records, name='clinic_records'),
    path('payments/', views.clinic_payments, name='clinic_payments'),

    # Auth
    path('register/', views.clinic_register, name='clinic_register'),
    path('login/', views.clinic_login_view, name='clinic_login'),
    path('logout/', views.clinic_logout_view, name='clinic_logout'),

    # Protected patient pages
    path('dashboard/', views.dashboard_view, name='clinic_dashboard'),
    path('patient-entry/', views.patient_entry, name='patient_entry'),
    path('existing-patients/', views.existing_patients, name='existing_patients'),
    path('prescriptions/', views.prescriptions_view, name='prescriptions'),

    # Doctor pages
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/update-status/<int:appointment_id>/<str:status>/', views.doctor_update_appointment_status,
         name='doctor_update_appointment_status'),
]