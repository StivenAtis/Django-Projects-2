"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Importación de módulos y vistas necesarias para la configuración de URLs en el proyecto.
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

# Definición de las URL del proyecto.
urlpatterns = [
    path('admin/', admin.site.urls),  # URL para la interfaz de administración de Django.

    # URLs para el registro y perfil de usuario.
    path('register/', user_views.register, name='register'),  # URL para el registro de nuevos usuarios.
    path('profile/', user_views.profile, name='profile'),     # URL para la página de perfil de usuario.

    # URLs para autenticación de usuario.
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # URL para inicio de sesión.
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),  # URL para cierre de sesión.
    
    # URLs para restablecimiento de contraseña.
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),  # URL para iniciar el restablecimiento de contraseña.
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),  # URL para confirmar que se ha enviado el correo de restablecimiento.
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),  # URL para confirmar el restablecimiento de contraseña.
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),  # URL para completar el restablecimiento de contraseña.

    # Inclusión de URLs para autenticación social con allauth.
    path('accounts/', include('allauth.urls')),  # URLs para el manejo de cuentas sociales.

    # Inclusión de URLs para otras aplicaciones del proyecto.
    path('', include('blog.urls')),               # URL para el blog.
    path('user/', include('users.urls')),         # URL para las funcionalidades de usuarios.
    path('notifications/', include('notification.urls')),  # URL para notificaciones.
    path('chats/', include('chat.urls')),         # URL para el chat.
    path('vc/', include('videocall.urls')),       # URL para videollamadas.
    path('friend/', include('friend.urls', namespace='friend')),  # URL para funcionalidades de amistad.
]

# Configuración para servir archivos de medios en modo de depuración.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Servir archivos de medios durante el desarrollo.


