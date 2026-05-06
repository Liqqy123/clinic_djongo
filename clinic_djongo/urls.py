from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect  # для редиректа

def root_home(request):
    return redirect('clinic_home')
urlpatterns = [
    path('', root_home, name='home'),
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),

]