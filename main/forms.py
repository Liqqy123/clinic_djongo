from django import forms
from django.utils import timezone
from .models import Appointment, Payment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'doctor', 'date', 'time', 'notes']
        widgets = {
            'patient_name': forms.TextInput(attrs={'placeholder': 'ФИО пациента', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Причина обращения', 'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'patient_name': 'Пациент',
            'doctor': 'Врач',
            'date': 'Дата приема',
            'time': 'Время приема',
            'notes': 'Описание',
        }

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        if selected_date and selected_date < timezone.localdate():
            raise forms.ValidationError('Дата приема не может быть в прошлом.')
        return selected_date


class RecordSearchForm(forms.Form):
    patient_name = forms.CharField(
        required=False,
        label='Пациент',
        widget=forms.TextInput(attrs={'placeholder': 'ФИО пациента', 'class': 'form-control'}),
    )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['appointment', 'amount', 'method']
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'appointment': 'Прием',
            'amount': 'Сумма',
            'method': 'Способ оплаты',
        }
