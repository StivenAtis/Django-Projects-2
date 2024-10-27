from django.apps import AppConfig  # Importa la clase AppConfig de Django, que se usa para configurar la aplicación.

class VideocallConfig(AppConfig):
    # Define el campo de clave primaria predeterminado para los modelos en esta aplicación.
    default_auto_field = 'django.db.models.BigAutoField'  
    
    # Especifica el nombre de la aplicación, que debe coincidir con el nombre de la carpeta de la aplicación.
    name = 'videocall'
