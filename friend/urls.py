from django.urls import path
from friend.views import (
    cancel_friend_request,  # Vista para cancelar una solicitud de amistad.
    decline_friend_request,  # Vista para rechazar una solicitud de amistad.
    friend_requests,  # Vista para mostrar solicitudes de amistad recibidas.
    friends_list_view,  # Vista para mostrar la lista de amigos.
    remove_friend,  # Vista para eliminar un amigo de la lista.
    send_friend_request,  # Vista para enviar una solicitud de amistad.
    accept_friend_request  # Vista para aceptar una solicitud de amistad.
)

app_name = "friend"  # Define el espacio de nombres para la aplicación de amigos.

urlpatterns = [
    path('list/<user_id>', friends_list_view, name='list'),  # Vista para mostrar la lista de amigos.
    path('friend_request/', send_friend_request, name="friend-request"),  # Vista para enviar una solicitud de amistad.
    path('friend_requests/<user_id>/', friend_requests, name='friend-requests'),  # Vista para mostrar solicitudes de amistad recibidas.
    path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),  # Vista para aceptar una solicitud de amistad.
    path('friend_remove/', remove_friend, name='remove-friend'),  # Vista para eliminar un amigo de la lista.
    path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),  # Vista para rechazar una solicitud de amistad.
    path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),  # Vista para cancelar una solicitud de amistad.
]