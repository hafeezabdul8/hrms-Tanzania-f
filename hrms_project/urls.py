from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='home'),  # Root → login
    path('', include('hrms_app.urls')),        # Your app URLs (dashboard, payslip, etc.)
    path('accounts/', include('django.contrib.auth.urls')),  # ← Built-in password reset under /accounts/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

