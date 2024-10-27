# Importación de módulos necesarios para crear modelos en Django.
from django.db import models
from django.contrib.auth.models import User  # Importación del modelo User para manejar usuarios.

""" Modelo para el Perfil de Usuario """
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User.
    is_online = models.BooleanField(default=False)  # Estado de conexión del usuario.
    following = models.ManyToManyField(User, related_name="following", blank=True)  # Usuarios a los que sigue.
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True)  # Amigos del usuario.
    bio = models.CharField(default="", blank=True, null=True, max_length=350)  # Biografía del usuario.
    date_of_birth = models.CharField(blank=True, max_length=150)  # Fecha de nacimiento del usuario.
    updated = models.DateTimeField(auto_now=True)  # Fecha de la última actualización.
    created = models.DateTimeField(auto_now_add=True)  # Fecha de creación del perfil.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)  # Imagen de perfil.

    # Método para obtener los posts del usuario asociado.
    def profile_posts(self):
        return self.user.post_set.all()  # Retorna todos los posts del usuario.

    # Método para obtener los amigos del usuario.
    def get_friends(self):
        return self.friends.all()  # Retorna la lista de amigos.

    # Método para contar el número de amigos del usuario.
    def get_friends_no(self):
        return self.friends.all().count()  # Retorna la cantidad de amigos.

    # Método para representar el objeto como una cadena.
    def __str__(self):
        return f'{self.user.username} Profile'  # Muestra el nombre de usuario y 'Profile'.

# Opciones de estado para las relaciones de amistad.
STATUS_CHOICES = (
    ('send', 'send'),  # Solicitud de amistad enviada.
    ('accepted', 'accepted')  # Solicitud de amistad aceptada.
)

# Modelo para gestionar relaciones de amistad entre perfiles de usuario.
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_sender')  # Perfil que envía la solicitud.
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_receiver')  # Perfil que recibe la solicitud.
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)  # Estado de la relación de amistad.
    updated = models.DateTimeField(auto_now=True)  # Fecha de la última actualización.
    created = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la relación.

    # Método para representar el objeto como una cadena.
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"  # Muestra el emisor, receptor y estado de la relación.
