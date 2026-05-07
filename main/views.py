from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm, RecordSearchForm, PaymentForm
from .auth_forms import PatientRegistrationForm, PatientLoginForm
from .models import Doctor, Appointment, MedicalRecord, Payment


def is_doctor(user):
    """Проверить, является ли пользователь врачом."""
    return hasattr(user, 'doctor_profile') and user.doctor_profile is not None


def register(request):
    if request.user.is_authenticated:
        # Если уже вошли, перенаправляем на правильный дашборд
        if is_doctor(request.user):
            return redirect('doctor_dashboard')
        return redirect('clinic_home')

    form = PatientRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('clinic_home')

    return render(request, 'clinic/components/register.html', {'form': form, 'hide_nav': True})


def patient_login(request):
    if request.user.is_authenticated:
        if is_doctor(request.user):
            return redirect('doctor_dashboard')
        return redirect('clinic_home')

    form = PatientLoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)

        # Перенаправляем врача на его дашборд
        if is_doctor(user):
            return redirect('doctor_dashboard')
        return redirect('clinic_home')

    return render(request, 'clinic/components/login.html', {'form': form, 'hide_nav': True})


def patient_logout(request):
    logout(request)
    return redirect('clinic_login')


@login_required(login_url='clinic_login')
def home(request):
    # Если это врач, перенаправляем на врачебный дашборд
    if is_doctor(request.user):
        return redirect('doctor_dashboard')

    doctors_count = Doctor.objects.count()
    appointments_count = Appointment.objects.filter(status='pending').count()
    records_count = MedicalRecord.objects.count()
    payments_count = Payment.objects.count()

    return render(request, 'clinic/components/home.html', {
        'doctors_count': doctors_count,
        'appointments_count': appointments_count,
        'records_count': records_count,
        'payments_count': payments_count,
    })


@login_required(login_url='clinic_login')
def doctor_dashboard(request):
    """Дашборд врача со всеми его записями."""
    if not is_doctor(request.user):
        return redirect('clinic_home')

    doctor = request.user.doctor_profile
    appointments = doctor.appointments.all().order_by('date', 'time')

    # Статистика
    total = appointments.count()
    pending = appointments.filter(status='pending').count()
    confirmed = appointments.filter(status='confirmed').count()
    cancelled = appointments.filter(status='cancelled').count()

    return render(request, 'clinic/components/doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'total': total,
        'pending': pending,
        'confirmed': confirmed,
        'cancelled': cancelled,
    })


@login_required(login_url='clinic_login')
def doctor_update_appointment_status(request, appointment_id, status):
    if not is_doctor(request.user):
        return redirect('clinic_home')

    doctor = request.user.doctor_profile
    allowed_statuses = {'pending', 'confirmed', 'cancelled'}
    if status not in allowed_statuses:
        return redirect('doctor_dashboard')

    appointment = Appointment.objects.filter(pk=appointment_id, doctor=doctor).first()
    if appointment and request.method == 'POST':
        appointment.status = status
        appointment.save()

    return redirect('doctor_dashboard')


@login_required(login_url='clinic_login')
def doctor_list(request):
    doctors = Doctor.objects.prefetch_related('schedules').all()
    return render(request, 'clinic/components/doctors.html', {'doctors': doctors})


@login_required(login_url='clinic_login')
def book_appointment(request):
    if is_doctor(request.user):
        return redirect('doctor_dashboard')

    appointment_form = AppointmentForm(request.POST or None)
    saved = False

    if request.method == 'POST' and appointment_form.is_valid():
        appointment_form.save()
        saved = True
        appointment_form = AppointmentForm()

    return render(request, 'clinic/components/appointments.html', {
        'form': appointment_form,
        'saved': saved,
    })


@login_required(login_url='clinic_login')
def medical_records(request):
    if is_doctor(request.user):
        return redirect('doctor_dashboard')

    search_form = RecordSearchForm(request.GET or None)

    return render(request, 'clinic/components/records.html', {
        'form': search_form,
    })


@login_required(login_url='clinic_login')
def payments(request):
    if is_doctor(request.user):
        return redirect('doctor_dashboard')

    payment_form = PaymentForm(request.POST or None)
    saved = False

    if request.method == 'POST' and payment_form.is_valid():
        payment_form.save()
        saved = True
        payment_form = PaymentForm()

    return render(request, 'clinic/components/payments.html', {
        'form': payment_form,
        'saved': saved,
    })
