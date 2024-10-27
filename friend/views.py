from django.shortcuts import redirect, render  # Importa las funciones para redirigir y renderizar vistas.
from django.http import HttpResponse  # Importa HttpResponse para enviar respuestas HTTP.
import json  # Importa json para manejar datos en formato JSON.
from django.contrib.auth.models import User  # Importa el modelo User para interactuar con usuarios.
from friend.models import FriendList, FriendRequest  # Importa los modelos FriendList y FriendRequest para manejar amistades.


# vista para mostrar la lista de amigos
def friends_list_view(request, *args, **kwargs):
    context = {}
    user = request.user  # Obtiene el usuario actualmente autenticado.
    
    if user.is_authenticated:  # Verifica si el usuario está autenticado.
        user_id = kwargs.get("user_id")  # Obtiene el ID del usuario a mostrar.
        
        if user_id:
            try:
                this_user = User.objects.get(pk=user_id)  # Intenta obtener el usuario por su ID.
                context['this_user'] = this_user  # Agrega el usuario al contexto.
            except User.DoesNotExist:
                return HttpResponse("El usuario no existe.")  # Maneja el caso en que el usuario no existe.
            
            try:
                friend_list = FriendList.objects.get(user=this_user)  # Intenta obtener la lista de amigos del usuario.
            except FriendList.DoesNotExist:
                return HttpResponse(f"No se pudo encontrar una lista de amigos para {this_user.username}")  # Maneja el caso en que la lista de amigos no existe.
            
            if user != this_user:  # Verifica si el usuario autenticado no es el mismo que 'this_user'.
                if not user in friend_list.friends.all():  # Verifica si el usuario autenticado es amigo del usuario mostrado.
                    return HttpResponse("Debes ser amigo para ver su lista de amigos.")  # Mensaje si no son amigos.
            
            friends = []  # Inicializa la lista de amigos.
            auth_user_friend_list = FriendList.objects.get(user=user)  # Obtiene la lista de amigos del usuario autenticado.
            
            for friend in friend_list.friends.all():  # Recorre los amigos en la lista de 'this_user'.
                friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))  # Agrega amigos a la lista, verificando si son amigos mutuos.
                
            context['friends'] = friends  # Agrega la lista de amigos al contexto.
    
    else:		
        return HttpResponse("Debes ser amigo para ver su lista de amigos.")  # Mensaje si no está autenticado.
    
    return render(request, "friend/friend_list.html", context)  # Renderiza la plantilla con el contexto.


# vista para mostrar solicitudes de amistad recibidas
def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user  # Obtiene el usuario actualmente autenticado.
    
    if user.is_authenticated:  # Verifica si el usuario está autenticado.
        user_id = kwargs.get("user_id")  # Obtiene el ID del usuario para el cual se solicitan las solicitudes de amistad.
        account = User.objects.get(pk=user_id)  # Intenta obtener el usuario correspondiente al ID.

        if account == user:  # Verifica si el usuario actual es el mismo que el que se está consultando.
            friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)  # Obtiene las solicitudes de amistad activas.
            context['friend_requests'] = friend_requests  # Agrega las solicitudes al contexto.
        else:
            return HttpResponse("No puedes ver la solicitud de amistad de otro usuario.")  # Mensaje si el usuario no tiene permiso.
    else:
        return redirect("login")  # Redirige al usuario a la página de inicio de sesión si no está autenticado.
    
    return render(request, "friend/friend_requests.html", context)  # Renderiza la plantilla con el contexto de solicitudes de amistad.



# vista para enviar una solicitud de amistad
def send_friend_request(request, *args, **kwargs):
    user = request.user  # Obtiene el usuario autenticado.
    payload = {}  # Inicializa el diccionario para la respuesta.

    if request.method == "POST" and user.is_authenticated:  # Verifica si la solicitud es POST y el usuario está autenticado.
        user_id = request.POST.get("receiver_user_id")  # Obtiene el ID del usuario receptor desde los datos POST.
        
        if user_id:  # Verifica que se haya proporcionado un ID de usuario receptor.
            receiver = User.objects.get(pk=user_id)  # Intenta obtener el usuario receptor.

            try:
                # Verifica si ya existe una solicitud activa de amistad del usuario actual al receptor.
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                
                for request in friend_requests:
                    if request.is_active:  # Si ya hay una solicitud activa, lanza una excepción.
                        raise Exception("Ya le enviaste una solicitud de amistad.")

                # Crea y guarda una nueva solicitud de amistad si no hay solicitudes activas.
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Solicitud de amistad enviada."
            
            except Exception as e:
                payload['response'] = str(e)  # Guarda el mensaje de error si ocurre una excepción.
        
        else:
            payload['response'] = "No se puede enviar la solicitud de amistad"  # Mensaje si no se proporcionó un ID de usuario.

    else:
        payload['response'] = "Debes estar autenticado para enviar una solicitud de amistad."  # Mensaje si el usuario no está autenticado.

    return HttpResponse(json.dumps(payload), content_type="application/json")  # Devuelve la respuesta en formato JSON.


# vista para aceptar una solicitud de amistad
def accept_friend_request(request, *args, **kwargs):
    user = request.user  # Obtiene el usuario autenticado.
    payload = {}  # Inicializa el diccionario para la respuesta.

    if request.method == "GET" and user.is_authenticated:  # Verifica si la solicitud es GET y el usuario está autenticado.
        friend_request_id = kwargs.get("friend_request_id")  # Obtiene el ID de la solicitud de amistad desde los parámetros.

        if friend_request_id:  # Verifica que se haya proporcionado un ID de solicitud.
            friend_request = FriendRequest.objects.get(pk=friend_request_id)  # Intenta obtener la solicitud de amistad.

            if friend_request.receiver == user:  # Verifica que el receptor de la solicitud sea el usuario autenticado.
                if friend_request:  # Verifica que la solicitud exista.
                    friend_request.accept()  # Acepta la solicitud de amistad.
                    payload['response'] = "Solicitud de amistad aceptada."  # Mensaje de éxito.
                else:
                    payload['response'] = "Algo salió mal."  # Mensaje si la solicitud no es válida.
            else:
                payload['response'] = "Esta no es tu petición para aceptar."  # Mensaje si la solicitud no es del usuario.
        else:
            payload['response'] = "No se puede aceptar la solicitud de amistad."  # Mensaje si no se proporciona un ID.

    else:
        payload['response'] = "Debes estar autenticado para aceptar una solicitud de amistad."  # Mensaje si el usuario no está autenticado.

    return HttpResponse(json.dumps(payload), content_type="application/json")  # Devuelve la respuesta en formato JSON.


# vista para eliminar un amigo de la lista
def remove_friend(request, *args, **kwargs):
    user = request.user  # Obtiene el usuario autenticado.
    payload = {}  # Inicializa el diccionario para la respuesta.

    if request.method == "POST" and user.is_authenticated:  # Verifica que la solicitud sea POST y el usuario esté autenticado.
        user_id = request.POST.get("receiver_user_id")  # Obtiene el ID del amigo a eliminar desde los datos de la solicitud.

        if user_id:  # Verifica que se haya proporcionado un ID de usuario.
            try:
                removee = User.objects.get(pk=user_id)  # Intenta obtener el usuario a eliminar.
                friend_list = FriendList.objects.get(user=user)  # Obtiene la lista de amigos del usuario.
                friend_list.unfriend(removee)  # Elimina al amigo de la lista.
                payload['response'] = "Amigo eliminado con éxito."  # Mensaje de éxito.
            except Exception as e:  # Maneja cualquier excepción que ocurra.
                payload['response'] = f"Algo salió mal: {str(e)}"  # Mensaje de error con detalles de la excepción.
        else:
            payload['response'] = "Se produjo un error. No se pudo eliminar a ese amigo."  # Mensaje si no se proporciona un ID.

    else:
        payload['response'] = "Debes estar autenticado para eliminar a un amigo."  # Mensaje si el usuario no está autenticado.

    return HttpResponse(json.dumps(payload), content_type="application/json")  # Devuelve la respuesta en formato JSON.


# vista para rechazar una solicitud de amistad
def decline_friend_request(request, *args, **kwargs):
    user = request.user  # Obtiene el usuario autenticado.
    payload = {}  # Inicializa el diccionario para la respuesta.

    if request.method == "GET" and user.is_authenticated:  # Verifica que la solicitud sea GET y el usuario esté autenticado.
        friend_request_id = kwargs.get("friend_request_id")  # Obtiene el ID de la solicitud de amistad a rechazar.

        if friend_request_id:  # Verifica que se haya proporcionado un ID de solicitud.
            friend_request = FriendRequest.objects.get(pk=friend_request_id)  # Intenta obtener la solicitud de amistad.

            if friend_request.receiver == user:  # Verifica que el receptor de la solicitud sea el usuario autenticado.
                if friend_request: 
                    friend_request.decline()  # Declina la solicitud de amistad.
                    payload['response'] = "Solicitud de amistad rechazada."  # Mensaje de éxito.
                else:
                    payload['response'] = "Algo salió mal."  # Mensaje de error si no se obtiene la solicitud.
            else:
                payload['response'] = "Esta no es una solicitud de amistad que puedas rechazar."  # Mensaje si la solicitud no pertenece al usuario.
        else:
            payload['response'] = "No se puede rechazar la solicitud de amistad."  # Mensaje si no se proporciona un ID.

    else:
        payload['response'] = "Debes estar autenticado para rechazar una solicitud de amistad."  # Mensaje si el usuario no está autenticado.

    return HttpResponse(json.dumps(payload), content_type="application/json")  # Devuelve la respuesta en formato JSON.


# vista para cancelar una solicitud de amistad
def cancel_friend_request(request, *args, **kwargs):
    user = request.user  # Obtiene el usuario autenticado.
    payload = {}  # Inicializa el diccionario para la respuesta.

    if request.method == "POST" and user.is_authenticated:  # Verifica que la solicitud sea POST y el usuario esté autenticado.
        user_id = request.POST.get("receiver_user_id")  # Obtiene el ID del receptor de la solicitud.

        if user_id:  # Verifica que se haya proporcionado un ID de usuario.
            receiver = User.objects.get(pk=user_id)  # Intenta obtener el usuario receptor.

            # Intenta obtener las solicitudes de amistad activas del usuario.
            friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)

            if not friend_requests:  # Si no hay solicitudes activas, responde con un mensaje.
                payload['response'] = "No hay nada que cancelar. La solicitud de amistad no existe."
            else:
                # Cancela todas las solicitudes de amistad encontradas.
                for friend_request in friend_requests:
                    friend_request.cancel()
                payload['response'] = "Solicitud de amistad cancelada."  # Mensaje de éxito.

        else:
            payload['response'] = "No se puede cancelar la solicitud de amistad."  # Mensaje si no se proporciona un ID.

    else:
        payload['response'] = "Debes estar autenticado para cancelar una solicitud de amistad."  # Mensaje si el usuario no está autenticado.

    return HttpResponse(json.dumps(payload), content_type="application/json")  # Devuelve la respuesta en formato JSON.