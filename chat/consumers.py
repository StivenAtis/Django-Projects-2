from chat.models import Chat, Room  # Importa los modelos Chat y Room desde la aplicación chat
import json  # Importa el módulo json para procesar datos en formato JSON
from channels.generic.websocket import AsyncWebsocketConsumer  # Importa el consumidor WebSocket asincrónico de Django Channels
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django para gestionar la autenticación de usuarios
from asgiref.sync import sync_to_async, async_to_sync  # Importa funciones para hacer la conversión entre síncrono y asíncrono


# Función para crear un nuevo mensaje en la base de datos
@sync_to_async
def create_new_message(me, friend, message, room_id):
    # Obtiene la sala correspondiente al room_id
    get_room = Room.objects.filter(room_id=room_id)[0]
    # Busca el autor y el amigo por su nombre de usuario
    author_user = User.objects.filter(username=me)[0]
    friend_user = User.objects.filter(username=friend)[0]
    # Crea un nuevo objeto Chat
    new_chat = Chat.objects.create(
        author=author_user,
        friend=friend_user,
        room_id=get_room,
        text=message
    )

# Clase ChatRoomConsumer para manejar la conexión y desconexión de los websockets
class ChatRoomConsumer(AsyncWebsocketConsumer):

    """Método para conectar al websocket"""
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']  # Nombre de la sala
        self.room_group_name = 'chat_%s' % self.room_name  # Grupo de la sala

        # Añade el canal al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # Acepta la conexión

    """Método para desconectar el websocket"""
    async def disconnect(self, close_code):
        # Elimina el canal del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    """Método para recibir mensajes"""
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  # Convierte el texto recibido a JSON
        message = text_data_json['message']  # Mensaje
        username = text_data_json['username']  # Nombre de usuario
        user_image = text_data_json['user_image']  # Imagen de usuario

        # Envía el mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
                'user_image': user_image,
            }
        )

    """Método para manejar el envío de mensajes"""
    async def chatroom_message(self, event):
        message = event['message']  # Mensaje del evento
        username = event['username']  # Nombre de usuario del evento
        user_image = event['user_image']  # Imagen de usuario del evento

        # Guarda el nuevo mensaje en la base de datos
        await create_new_message(me=self.scope["user"], friend=username, message=message, room_id=self.room_name)

        # Envía el mensaje al cliente
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'user_image': user_image,
        }))