from django.db import models  # Importa el módulo models de Django para definir modelos de datos.

# Crea el modelo RoomMember para almacenar información sobre los miembros de la sala.
class RoomMember(models.Model):
    # Nombre del miembro de la sala, se almacena como un campo de texto con un límite de 200 caracteres.
    name = models.CharField(max_length=200)  
    
    # Identificador único del miembro de la sala (UID), se almacena como un campo de texto con un límite de 1000 caracteres.
    uid = models.CharField(max_length=1000)  
    
    # Nombre de la sala en la que el miembro está participando, se almacena como un campo de texto con un límite de 200 caracteres.
    room_name = models.CharField(max_length=200)  
    
    # Indica si el miembro está actualmente en una sesión. Por defecto, este valor es True.
    insession = models.BooleanField(default=True)  

    def __str__(self):
        # Devuelve el nombre del miembro como representación en cadena del objeto.
        return self.name
