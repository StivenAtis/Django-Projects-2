from django.contrib import admin  # Importa el módulo admin de Django, que permite gestionar el panel de administración.

# Importa el modelo RoomMember desde el archivo models.py en la misma aplicación.
from .models import RoomMember

# Registra el modelo RoomMember en el sitio de administración de Django.
# Esto permitirá que el modelo sea gestionado a través de la interfaz de administración.
admin.site.register(RoomMember)
