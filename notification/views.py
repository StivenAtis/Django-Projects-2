# Importación de módulos y decoradores necesarios para la vista de notificaciones.
from django.contrib.auth.decorators import login_required  # Decorador para requerir autenticación del usuario.
from django.shortcuts import render  # Función para renderizar plantillas.
from django.http import HttpResponse  # Clase para respuestas HTTP.
from notification.models import Notification  # Importación del modelo Notification.

# Vista para mostrar todas las notificaciones del usuario autenticado.
@login_required  # Asegura que solo los usuarios autenticados puedan acceder a esta vista.
def ShowNotifications(request):
    user = request.user  # Obtiene el usuario actual de la solicitud.
    
    # Filtra las notificaciones del usuario y las ordena por fecha, de más reciente a más antiguo.
    notifications = Notification.objects.filter(user=user).order_by('-date')  
    context = {
        'notifications': notifications,  # Contexto para la plantilla que incluye las notificaciones.
    }
    
    # Renderiza la plantilla de notificaciones con el contexto proporcionado.
    return render(request, 'blog/notifications.html', context)
