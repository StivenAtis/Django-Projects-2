# Importación de módulos necesarios para la configuración de URLs en la aplicación de notificaciones.
from django.urls import path
from notification.views import ShowNotifications  # Importación de la vista para mostrar notificaciones.

# Definición de las URL de la aplicación de notificaciones.
urlpatterns = [
    path('', ShowNotifications, name='show-notifications'),  # URL para mostrar todas las notificaciones.
]