from django.contrib import admin  # Importa el módulo de administración de Django
from .models import Comment, Post  # Importa los modelos Comment y Post del archivo models.py

# Registra el modelo Post en el sitio de administración de Django
admin.site.register(Post)

# Registra el modelo Comment en el sitio de administración de Django
admin.site.register(Comment)
