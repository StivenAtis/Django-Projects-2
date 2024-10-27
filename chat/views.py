from django.shortcuts import render, redirect  # Importa render y redirect para manejar respuestas HTTP y redirecciones
from django.contrib.auth.decorators import login_required  # Decorador para restringir vistas solo a usuarios autenticados
from django.contrib import messages  # Importa messages para mostrar mensajes de error o éxito
from .models import Room, Chat  # Importa los modelos Room y Chat para interactuar con la base de datos
from django.db.models import Q  # Importa Q para realizar consultas complejas
from friend.models import FriendList  # Importa FriendList para acceder a la lista de amigos del usuario
from django.contrib.auth.models import User  # Importa el modelo User para acceder a usuarios

# Vista para inscribir o unir a un usuario en una sala de chat
@login_required
def room_enroll(request):
    friends = FriendList.objects.filter(user=request.user)[0].friends.all()  # Obtiene todos los amigos del usuario
    all_rooms = Room.objects.filter(
        Q(author=request.user) | Q(friend=request.user)  # Filtra salas de chat donde el usuario es autor o amigo
    ).order_by('-created')  # Ordena las salas por fecha de creación en orden descendente

    context = {
        'all_rooms': all_rooms,  # Salas en las que participa el usuario
        'all_friends': friends,  # Lista de amigos del usuario
    }
    return render(request, 'chat/join_room.html', context)  # Renderiza la plantilla join_room.html con el contexto


# Vista para elegir o crear una sala de chat con un amigo específico
@login_required
def room_choice(request, friend_id):
    friend = User.objects.filter(pk=friend_id)  # Verifica si existe un usuario con el ID proporcionado
    if not friend:
        messages.error(request, 'Invalid User ID')  # Muestra un mensaje de error si el usuario no existe
        return redirect('room-enroll') 

    if not FriendList.objects.filter(user=request.user, friends=friend[0]):  # Verifica si el usuario es amigo
        messages.error(request, 'You need to be friends to chat')  # Muestra un mensaje de error si no son amigos
        return redirect('room-enroll') 

    room = Room.objects.filter(
        Q(author=request.user, friend=friend[0]) | Q(author=friend[0], friend=request.user)  # Filtra la sala entre ambos usuarios
    )
    if not room:
        create_room = Room(author=request.user, friend=friend[0])  # Crea una nueva sala si no existe
        create_room.save()  # Guarda la sala en la base de datos
        room = create_room.room_id  # Asigna el ID de la sala recién creada
        return redirect('room', room, friend_id)  # Redirige a la sala recién creada

    return redirect('room', room[0].room_id, friend_id)  # Redirige a la sala existente entre ambos usuarios


""" Sala de chat entre usuarios """
@login_required
def room(request, room_name, friend_id):
    all_rooms = Room.objects.filter(room_id=room_name)  # Verifica si la sala de chat existe
    if not all_rooms:  
        messages.error(request, 'Invalid Room ID')  # Muestra un mensaje de error si la sala no existe
        return redirect('room-enroll')

    chats = Chat.objects.filter(
        room_id=room_name  # Obtiene todos los mensajes de la sala de chat ordenados por fecha
    ).order_by('date')

    context = {
        'old_chats': chats,  # Mensajes antiguos en la sala
        'my_name': request.user,  # Nombre del usuario actual
        'friend_name': User.objects.get(pk=friend_id),  # Nombre del amigo en la sala de chat
        'room_name': room_name  # ID de la sala de chat
    }
    return render(request, 'chat/chatroom.html', context)  # Renderiza la plantilla chatroom.html con el contexto
