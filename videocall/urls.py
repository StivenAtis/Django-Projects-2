from django.urls import path  # Importa la función path para definir las rutas de la aplicación.
from . import views  # Importa las vistas definidas en el archivo views.py.

# Define las URL y sus correspondientes vistas para la aplicación de videollamadas.
urlpatterns = [
    # Ruta para la sala de espera (lobby) de la videollamada. Llama a la vista 'lobby' y se identifica con el nombre 'vc-lobby'.
    path('', views.lobby, name='vc-lobby'),  
    
    # Ruta para la sala de videollamada. Llama a la vista 'room' y se identifica con el nombre 'vc-room'.
    path('room/', views.room, name='vc-room'),  
    
    # Ruta para obtener un token de acceso para la sala de videollamada. Llama a la vista 'getToken'.
    path('get_token/', views.getToken),  
    
    # Ruta para crear un nuevo miembro en la sala de videollamada. Llama a la vista 'createMember'.
    path('create_member/', views.createMember),  
    
    # Ruta para obtener la información de un miembro específico de la sala. Llama a la vista 'getMember'.
    path('get_member/', views.getMember),  
    
    # Ruta para eliminar un miembro de la sala de videollamada. Llama a la vista 'deleteMember'.
    path('delete_member/', views.deleteMember),  
]