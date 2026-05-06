from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient_name', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }