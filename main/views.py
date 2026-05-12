from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Doctor, Patient, Prescription, Appointment, Payment
from .forms import RegistrationForm, LoginForm, PatientEntryForm, AppointmentForm, PaymentForm, PrescriptionForm

def home(request):
    context = {
        'popular_services': ['УЗИ', 'КТ', 'МРТ', 'Гастроскопия'],
        'popular_directions': ['Акушерство-гинекология', 'Кардиология', ...],
    }
    return render(request, 'pages/home.html', context)

def doctors_list(request):
    doctors = Doctor.objects.all()  # ваша модель
    if request.GET.get('search'):
        doctors = doctors.filter(name__icontains=request.GET['search'])
    return render(request, 'pages/doctors_list.html', {'doctors': doctors})

def doctor_detail(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    return render(request, 'pages/doctor_detail.html', {'doctor': doctor})
def clinics(request):
    return render(request, 'pages/clinics.html', {'title': 'Клиники'})

def promotions(request):
    return render(request, 'pages/promotions.html', {'title': 'Акции'})

def services(request):
    return render(request, 'pages/services.html', {'title': 'Услуги'})
def clinic_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})

def clinic_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'pages/register.html', {'form': form})

def clinic_logout_view(request):
    logout(request)
    return redirect('home')