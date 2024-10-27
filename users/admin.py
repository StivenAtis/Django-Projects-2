# Importación del módulo de administración de Django y los modelos Profile y Relationship.
from django.contrib import admin
from .models import Profile, Relationship  # Importación de los modelos de perfil y relación.

# Registro de los modelos en el sitio de administración de Django.
admin.site.register(Profile)        # Permite la gestión de perfiles de usuario en la interfaz de administración.
admin.site.register(Relationship)   # Permite la gestión de relaciones entre usuarios en la interfaz de administración.
