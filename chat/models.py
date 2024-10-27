from django.db import models  # Importa el módulo de modelos de Django para definir las estructuras de datos
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django para relacionarlo con los chats y salas
import uuid  # Importa uuid para la creación de identificadores únicos si fuera necesario

# Define los modelos para la aplicación de chat

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)  # Campo de clave primaria para identificar cada sala
    author = models.ForeignKey(User, related_name='author_room', on_delete=models.CASCADE)  # Usuario que creó la sala
    friend = models.ForeignKey(User, related_name='friend_room', on_delete=models.CASCADE)  # Usuario invitado o amigo
    created = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la sala

    def __str__(self):
        return f"{self.room_id}-{self.author}-{self.friend}"  # Representación en string de la sala para facilitar su identificación


class Chat(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats')  # Sala a la que pertenece el mensaje
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_msg')  # Usuario que envió el mensaje
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_msg')  # Usuario destinatario o amigo
    text = models.CharField(max_length=300)  # Contenido del mensaje con un límite de 300 caracteres
    date = models.DateTimeField(auto_now_add=True)  # Fecha de envío del mensaje
    has_seen = models.BooleanField(default=False)  # Campo booleano para saber si el mensaje ha sido leído

    def __str__(self):
        return '%s - %s' % (self.id, self.date)  # Representación en string del mensaje, incluye el id y la fecha de envío
