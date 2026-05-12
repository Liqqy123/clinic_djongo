from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Patient, Appointment, Payment, Prescription

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=100, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', max_length=20, required=True)
    address = forms.CharField(label='Адрес', widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PatientEntryForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'age', 'gender', 'phone', 'email', 'address', 'allergies',
                  'medical_history']
        widgets = {
            'patient_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: P001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Возраст'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Адрес'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Аллергии'}),
            'medical_history': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Медицинская история'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_phone', 'doctor', 'date', 'time', 'notes']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['patient_name', 'patient_phone', 'doctor', 'amount', 'purpose']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_id', 'patient', 'doctor', 'diagnosis', 'medications', 'notes', 'status']
        widgets = {
            'prescription_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: RX001'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Диагноз'}),
            'medications': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Лекарства и дозировка'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Дополнительные заметки'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }