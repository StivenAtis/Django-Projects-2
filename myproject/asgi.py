"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

"""
ASGI (Asynchronous Server Gateway Interface) es un estándar para manejar aplicaciones web en Python de manera asíncrona.
ASGI permite manejar tanto comunicaciones HTTP como protocolos de tiempo real, como WebSockets, además de otras conexiones asíncronas.
"""

# Importa el módulo os para interactuar con el sistema operativo.
import os

# Importa la función get_asgi_application para manejar solicitudes asíncronas en Django.
from django.core.asgi import get_asgi_application

# Establece el módulo de configuración predeterminado de Django para el proyecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Crea una instancia de la aplicación ASGI, que Django usará para manejar solicitudes.
application = get_asgi_application()
