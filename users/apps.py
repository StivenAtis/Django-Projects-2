# Configuración de la aplicación de usuarios en Django.
from django.apps import AppConfig

# Clase de configuración para la aplicación de usuarios.
class UsersConfig(AppConfig):
    name = 'users'  # Nombre de la aplicación, utilizado por Django para referenciarla.

    def ready(self):
        # Importa señales cuando la aplicación está lista.
        import users.signals  # Importación de señales para manejar eventos específicos relacionados con usuarios.
