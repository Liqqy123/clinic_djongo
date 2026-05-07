
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Doctor, Patient, Prescription, Appointment, Payment
from .forms import RegistrationForm, LoginForm, PatientEntryForm, AppointmentForm, PaymentForm, PrescriptionForm


def is_doctor(user):
    return hasattr(user, 'doctor_profile') and user.doctor_profile is not None


def clinic_home(request):
    doctors = Doctor.objects.all()[:3]
    context = {
        'doctors': doctors,
        'total_patients': Patient.objects.count(),
        'active_patients': Patient.objects.filter(is_active=True).count(),
        'prescriptions_today': Prescription.objects.filter(issue_date=timezone.now().date()).count(),
    }
    return render(request, 'main/home.html', context)


def clinic_doctors(request):
    doctors = Doctor.objects.all().prefetch_related('schedules')
    return render(request, 'main/doctors.html', {'doctors': doctors})


def clinic_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('clinic_home')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def clinic_login_view(request):
    if request.user.is_authenticated:
        if is_doctor(request.user):
            return redirect('doctor_dashboard')
        return redirect('clinic_home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if is_doctor(user):
                return redirect('doctor_dashboard')
            return redirect('clinic_home')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def clinic_logout_view(request):
    logout(request)
    return redirect('clinic_login')


@login_required
def dashboard_view(request):
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(is_active=True).count()
    total_prescriptions = Prescription.objects.count()
    today = timezone.now().date()
    prescriptions_today = Prescription.objects.filter(issue_date=today).count()

    recent_patients = Patient.objects.order_by('-created_at')[:5]
    recent_prescriptions = Prescription.objects.select_related('patient').order_by('-issue_date')[:5]

    context = {
        'total_patients': total_patients,
        'active_patients': active_patients,
        'total_prescriptions': total_prescriptions,
        'prescriptions_today': prescriptions_today,
        'recent_patients': recent_patients,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def patient_entry(request):
    if request.method == 'POST':
        form = PatientEntryForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Пациент {patient.full_name} успешно зарегистрирован!')
            return redirect('existing_patients')
    else:
        # Auto-generate patient ID
        last_patient = Patient.objects.order_by('-patient_id').first()
        if last_patient and last_patient.patient_id.startswith('P'):
            try:
                last_num = int(last_patient.patient_id[1:])
                new_id = f"P{last_num + 1:03d}"
            except:
                new_id = "P001"
        else:
            new_id = "P001"

        form = PatientEntryForm(initial={'patient_id': new_id})

    return render(request, 'main/patient_entry.html', {'form': form})


@login_required
def existing_patients(request):
    search_query = request.GET.get('search', '')
    patients = Patient.objects.all()

    if search_query:
        patients = patients.filter(
            Q(patient_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(is_active=True).count()
    today = timezone.now().date()
    new_today = Patient.objects.filter(created_at__date=today).count()

    context = {
        'patients': patients,
        'search_query': search_query,
        'total_patients': total_patients,
        'active_patients': active_patients,
        'new_today': new_today,
    }
    return render(request, 'main/existing_patients.html', context)


@login_required
def prescriptions_view(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    prescriptions = Prescription.objects.select_related('patient', 'doctor').all()

    if search_query:
        prescriptions = prescriptions.filter(
            Q(prescription_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__patient_id__icontains=search_query) |
            Q(patient__phone__icontains=search_query)
        )

    if status_filter:
        prescriptions = prescriptions.filter(status=status_filter)

    total = Prescription.objects.count()
    active = Prescription.objects.filter(status='active').count()
    completed = Prescription.objects.filter(status='completed').count()

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецепт успешно создан!')
            return redirect('prescriptions')
    else:
        form = PrescriptionForm()

    context = {
        'prescriptions': prescriptions,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_prescriptions': total,
        'active_prescriptions': active,
        'completed_prescriptions': completed,
        'form': form,
    }
    return render(request, 'main/prescriptions.html', context)


def clinic_appointments(request):
    saved = False
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            saved = True
            messages.success(request, 'Вы успешно записаны на прием!')
            form = AppointmentForm()
    else:
        form = AppointmentForm()

    return render(request, 'main/appointments.html', {'form': form, 'saved': saved})


def clinic_records(request):
    return render(request, 'main/records.html')


def clinic_payments(request):
    saved = False
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.status = 'paid'  # Auto-confirm for demo
            payment.save()
            saved = True
            messages.success(request, 'Оплата прошла успешно!')
            form = PaymentForm()
    else:
        form = PaymentForm()

    return render(request, 'main/payments.html', {'form': form, 'saved': saved})


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    doctor = request.user.doctor_profile
    appointments = doctor.appointments.all().order_by('-date', '-time')

    total = appointments.count()
    pending = appointments.filter(status='pending').count()
    confirmed = appointments.filter(status='confirmed').count()
    cancelled = appointments.filter(status='cancelled').count()

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'total': total,
        'pending': pending,
        'confirmed': confirmed,
        'cancelled': cancelled,
    }
    return render(request, 'main/dashboard.html', context)


@login_required
@user_passes_test(is_doctor)
def doctor_update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)
    if status in ['pending', 'confirmed', 'cancelled', 'completed']:
        appointment.status = status
        appointment.save()
        messages.success(request, f'Статус записи изменен на {appointment.get_status_display()}')
    return redirect('doctor_dashboard')