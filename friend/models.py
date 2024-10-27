from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User # Importa el modelo User de Django para la autenticación.


""" Modelo de lista de amigos """
class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')  # Relación uno a uno con el modelo User.
    friends = models.ManyToManyField(User, blank=True, related_name='friends')  # Amigos del usuario.

    def __str__(self):
        return self.user.username  # Devuelve el nombre de usuario.

    def add_friend(self, account):
        if not account in self.friends.all():  # Verifica si el amigo ya está en la lista.
            self.friends.add(account)  # Agrega un amigo.
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():  # Verifica si el amigo está en la lista.
            self.friends.remove(account)  # Elimina un amigo.
            self.save()

    def unfriend(self, removee):
        remover_friends_list = self  # Lista de amigos del usuario que está eliminando.
        remover_friends_list.remove_friend(removee)  # Elimina al amigo.

        friends_list = FriendList.objects.get(user=removee)  # Obtiene la lista de amigos del amigo eliminado.
        friends_list.remove_friend(self.user)  # Elimina al usuario de la lista del amigo.

    def is_mutual_friend(self, friend):
        return friend in self.friends.all()  # Verifica si son amigos mutuos.


""" Modelo de solicitud de amistad """
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')  # Usuario que envía la solicitud.
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')  # Usuario que recibe la solicitud.
    is_active = models.BooleanField(blank=True, null=True, default=True)  # Estado de la solicitud.
    timestamp = models.DateTimeField(auto_now_add=True)  # Marca de tiempo de la solicitud.

    def __str__(self):
        return self.sender.username  # Devuelve el nombre del usuario que envió la solicitud.

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)  # Obtiene la lista de amigos del receptor.
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)  # Agrega al remitente a la lista de amigos del receptor.
            sender_friend_list = FriendList.objects.get(user=self.sender)  # Obtiene la lista de amigos del remitente.
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)  # Agrega al receptor a la lista de amigos del remitente.
                self.is_active = False  # Marca la solicitud como inactiva.
                self.save()

    def decline(self):
        self.is_active = False  # Marca la solicitud como inactiva.
        self.save()

    def cancel(self):
        self.is_active = False  # Marca la solicitud como inactiva.
        self.save()