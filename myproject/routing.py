# Importa el middleware de autenticación para WebSockets.
from channels.auth import AuthMiddlewareStack

# Importa los enrutadores de protocolo y URL para manejar diferentes tipos de conexión.
from channels.routing import ProtocolTypeRouter, URLRouter

# Importa las rutas de WebSocket desde la configuración del enrutamiento de la aplicación de chat.
import chat.routing

# Configura la aplicación para manejar diferentes protocolos.
application = ProtocolTypeRouter({
    # Define el manejo de conexiones WebSocket con autenticación y enrutamiento.
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # Aplica las rutas de WebSocket definidas en la aplicación de chat.
        )
    ),
})
