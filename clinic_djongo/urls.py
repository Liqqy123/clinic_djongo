from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

def root_home(request):
    return redirect('clinic_home')
urlpatterns = [
    path('', root_home, name='home'),
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


