from django.shortcuts import render
from django.http import HttpResponse
from .models import Doctor, Appointment  # ← импортируем модели
from .forms import AppointmentForm


def home(request):
    form = AppointmentForm()
    appointments = Appointment.objects.all()[:5]
    doctors = Doctor.objects.all()

    return render(request, 'clinic/home.html', {
        'form': form,
        'appointments': appointments,
        'doctors': doctors,
    })

