from main.models import Doctor, Patient

def user_role(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            role = 'Администратор'
        elif hasattr(request.user, 'doctor_profile'):
            role = 'Врач'
        elif hasattr(request.user, 'patient_profile'):
            role = 'Пациент'
        else:
            role = 'Пользователь'
        return {
            'user_role': role,
            'user_full_name': request.user.full_name or request.user.username,
        }
    return {}