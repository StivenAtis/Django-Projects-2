from enum import Enum

class FriendRequestStatus(Enum):
    NO_REQUEST_SENT = -1  # No se ha enviado ninguna solicitud de amistad.
    THEM_SENT_TO_YOU = 0  # Ellos enviaron una solicitud de amistad a ti.
    YOU_SENT_TO_THEM = 1  # Tú enviaste una solicitud de amistad a ellos.