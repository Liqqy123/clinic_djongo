from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctor/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('clinics/', views.clinics, name='clinics'),
    path('promotions/', views.promotions, name='promotions'),
    path('services/', views.services, name='services'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)