from django.urls import re_path  # Importa re_path para definir rutas URL con expresiones regulares

from . import consumers  # Importa el archivo de consumers que contiene la lógica del WebSocket

# Define el patrón de URL para las conexiones WebSocket
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),  # Ruta WebSocket para las salas de chat, usando room_name como parámetro
]
