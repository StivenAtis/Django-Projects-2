from friend.models import FriendRequest  # Importa el modelo FriendRequest para interactuar con la base de datos.

def get_friend_request_or_false(sender, receiver):
    """
    Intenta obtener una solicitud de amistad activa entre el remitente y el receptor.
    
    :param sender: El usuario que envió la solicitud.
    :param receiver: El usuario que recibió la solicitud.
    :return: La solicitud de amistad si existe, de lo contrario, devuelve False.
    """
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)  # Busca la solicitud activa.
    except FriendRequest.DoesNotExist:
        return False  # Retorna False si no se encuentra la solicitud.
