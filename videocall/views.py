import os  # Importa el módulo para acceder a las variables de entorno.
from django.shortcuts import redirect, render  # Importa funciones para redirigir y renderizar plantillas.
from django.http import JsonResponse  # Importa JsonResponse para enviar respuestas en formato JSON.
import random  # Importa módulo para generar números aleatorios.
import time  # Importa módulo para trabajar con tiempo.
from agora_token_builder import RtcTokenBuilder  # Importa la clase para generar tokens de Agora.

from friend.models import FriendList  # Importa el modelo FriendList para gestionar amigos.
from .models import RoomMember  # Importa el modelo RoomMember para gestionar miembros de la sala.
import json  # Importa módulo para trabajar con datos en formato JSON.
from django.views.decorators.csrf import csrf_exempt  # Importa decorador para omitir la protección CSRF.


# Vista del lobby donde se muestran los amigos del usuario.
def lobby(request):
    friends = FriendList.objects.filter(user=request.user)[0].friends.all()  # Obtiene la lista de amigos.
    context = {
        'friends': friends  # Pasa la lista de amigos al contexto.
    }
    return render(request, 'videocall/lobby.html', context)  # Renderiza la plantilla del lobby.

# Vista de la sala de videollamadas.
def room(request):
    return render(request, 'videocall/room.html')  # Renderiza la plantilla de la sala.


# Función para validar si la llamada es de un amigo.
def validateVC(request, vc_to):
    # Obtiene la lista de amigos del usuario actual.
    friends = FriendList.objects.filter(user=request.user)[0].friends.all()
    id_list = list(friends.values_list('id', flat=True))  # Crea una lista con los IDs de amigos.
    
    # Verifica si el ID de la persona a la que se quiere llamar está en la lista de amigos.
    if vc_to in id_list:
        return True  # Llamada válida.
    else:
        return False  # Llamada no válida.


# Vista para obtener un token de acceso a la sala de videollamadas.
def getToken(request):
    appId = os.environ.get('AGORA_APP_ID')  # Obtiene el ID de la aplicación desde las variables de entorno.
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')  # Obtiene el certificado de la aplicación desde las variables de entorno.
    channelName = request.GET.get('channel')  # Obtiene el nombre del canal desde los parámetros de la solicitud.

    # Valida si el ID de la llamada es de un amigo.
    try:
        if validateVC(request, int(channelName)):
            pass
        else:
            return JsonResponse(status=404, data={'status': 'false', 'message': 'ID mismatch'})
    except:
        return JsonResponse(status=404, data={'status': 'false', 'message': 'ID mismatch'})

    vc_to = channelName  # ID de la persona a la que se llama.
    vc_from = request.user.id  # ID del usuario que realiza la llamada.

    # Crea el nombre de la sala de videollamada.
    room_name = "VCROOM_" + str(vc_to) + "_" + str(vc_from) if int(vc_to) < int(vc_from) else "VCROOM_" + str(vc_from) + "_" + str(vc_to)

    uid = random.randint(1, 230)  # Genera un UID aleatorio para el usuario.
    expirationTimeInSeconds = 3600  # Tiempo de expiración del token en segundos.
    currentTimeStamp = int(time.time())  # Obtiene la marca de tiempo actual.
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds  # Calcula el tiempo de expiración del privilegio.
    role = 1  # Rol del usuario (1: usuario).

    # Genera el token de Agora utilizando los parámetros definidos.
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, room_name, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid, 'room_name': room_name}, safe=False)  # Devuelve el token, UID y nombre de la sala en formato JSON.


# Vista para crear un nuevo miembro en la sala de videollamadas.
@csrf_exempt
def createMember(request):
    data = json.loads(request.body)  # Carga los datos de la solicitud en formato JSON.
    member, created = RoomMember.objects.get_or_create(  # Crea o obtiene un miembro de la sala.
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)  # Devuelve el nombre del miembro en formato JSON.


# Vista para obtener la información de un miembro específico de la sala.
def getMember(request):
    uid = request.GET.get('UID')  # Obtiene el UID del miembro desde los parámetros de la solicitud.
    room_name = request.GET.get('room_name')  # Obtiene el nombre de la sala.

    member = RoomMember.objects.get(  # Obtiene el miembro basado en UID y nombre de la sala.
        uid=uid,
        room_name=room_name,
    )
    name = member.name  # Almacena el nombre del miembro.
    return JsonResponse({'name': member.name}, safe=False)  # Devuelve el nombre del miembro en formato JSON.


# Vista para eliminar un miembro de la sala de videollamadas.
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)  # Carga los datos de la solicitud en formato JSON.
    member = RoomMember.objects.get(  # Obtiene el miembro basado en el nombre, UID y nombre de la sala.
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()  # Elimina el miembro de la base de datos.
    return JsonResponse('Member deleted', safe=False)  # Devuelve un mensaje de confirmación en formato JSON.