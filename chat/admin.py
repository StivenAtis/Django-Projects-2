from django.contrib import admin
from .models import Chat, Room

# Registra el modelo Chat en el panel de administración de Django
admin.site.register(Chat)

# Registra el modelo Room en el panel de administración de Django
admin.site.register(Room)