# Importación del módulo de administración de Django y del modelo Notification.
from django.contrib import admin
from .models import Notification  # Importación del modelo de notificación.

# Registro del modelo Notification en el sitio de administración de Django.
admin.site.register(Notification)  # Permite la gestión de notificaciones a través de la interfaz de administración.
