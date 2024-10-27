# Importación de señales y modelos necesarios para manejar eventos en Django.
from django.db.models.signals import post_save  # Señal para acciones post-guardado de un modelo.
from django.contrib.auth.models import User  # Importación del modelo User para manejar usuarios.
from django.dispatch import receiver  # Decorador para conectar señales con funciones.
from .models import Profile, Relationship  # Importación de los modelos Profile y Relationship.
from friend.models import FriendList  # Importación del modelo FriendList.

""" Creación de perfil cuando un usuario crea una cuenta """
@receiver(post_save, sender=User)  # Conectar la señal post_save con la función create_profile.
def create_profile(sender, instance, created, **kwargs):
    if created:  # Verificar si el usuario ha sido creado.
        Profile.objects.create(user=instance)  # Crear un perfil asociado al usuario.


""" Guardar perfil cuando un usuario actualiza su cuenta """
@receiver(post_save, sender=User)  # Conectar la señal post_save con la función save_profile.
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # Guardar el perfil del usuario actualizado.

""" Agregar amigos a la lista de amigos cuando se acepta una solicitud """
@receiver(post_save, sender=Relationship)  # Conectar la señal post_save con la función post_save_add_to_friends.
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender  # Obtener el perfil del emisor de la solicitud.
    receiver_ = instance.receiver  # Obtener el perfil del receptor de la solicitud.
    if instance.status == 'accepted':  # Verificar si la relación ha sido aceptada.
        sender_.friends.add(receiver_.user)  # Agregar el receptor a la lista de amigos del emisor.
        receiver_.friends.add(sender_.user)  # Agregar el emisor a la lista de amigos del receptor.
        sender_.save()  # Guardar cambios en el perfil del emisor.
        receiver_.save()  # Guardar cambios en el perfil del receptor.


""" Creación de lista de amigos cuando un usuario crea una cuenta """
@receiver(post_save, sender=User)  # Conectar la señal post_save con la función create_friendlist.
def create_friendlist(sender, instance, created, **kwargs):
    if created:  # Verificar si el usuario ha sido creado.
        FriendList.objects.create(user=instance)  # Crear una lista de amigos asociada al usuario.