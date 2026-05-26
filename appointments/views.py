from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointments_list(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'appointments/list.html', {'appointments': appointments})

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('appointments:list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create.html', {'form': form})

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if appointment.status != 'cancelled':
        appointment.status = 'cancelled'
        appointment.save()
        messages.warning(request, 'Запись отменена.')
    return redirect('appointments:list')