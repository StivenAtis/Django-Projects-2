"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

# Importación de módulos necesarios para la configuración WSGI de Django.
import os
from django.core.wsgi import get_wsgi_application  # Función para obtener la aplicación WSGI.

# Establecimiento del módulo de configuración de Django a utilizar.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Configuración predeterminada del módulo de ajustes.

# Obtención de la aplicación WSGI para manejar solicitudes HTTP.
application = get_wsgi_application()  # Aplicación WSGI que será utilizada por el servidor web.
