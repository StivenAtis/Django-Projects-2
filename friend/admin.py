from django.contrib import admin
from friend.models import FriendList, FriendRequest

# Registra los modelos FriendList y FriendRequest en el panel de administración de Django.
admin.site.register(FriendList)  # Permite la gestión de listas de amigos en el admin.
admin.site.register(FriendRequest)  # Permite la gestión de solicitudes de amistad en el admin.
