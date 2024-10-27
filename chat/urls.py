from django.urls import path  # Importa path para definir rutas URL

from . import views  # Importa el archivo de vistas para conectar las rutas con las vistas correspondientes

# Define las rutas URL para la aplicación
urlpatterns = [
    path('', views.room_enroll, name='room-enroll'),  # Ruta para la inscripción a una sala de chat, apunta a la vista room_enroll
    path('chat/<int:friend_id>', views.room_choice, name='room-choice'),  # Ruta para elegir una sala de chat con un amigo específico
    path('room/<int:room_name>-<int:friend_id>', views.room, name='room'),  # Ruta para acceder a una sala de chat específica por nombre de sala y ID de amigo
]