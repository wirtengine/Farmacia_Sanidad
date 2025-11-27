"""
URL configuration for farmacia_site project.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios import views as usuarios_views  # Importa las vistas de usuarios

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Login como primera pantalla (URL raíz)
    path('', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    
    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Registro de nuevos usuarios
    path('registro/', usuarios_views.registro, name='registro'),
    
    # Incluye las rutas de farmacia_app bajo /farmacia/
    path('farmacia/', include('farmacia_app.urls')),
]