from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from friend.models import FriendList, FriendRequest


def friends_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id:
            try:
                this_user = User.objects.get(pk=user_id)
                context['this_user'] = this_user
            except User.DoesNotExist:
                return HttpResponse("El usuario no existe.")
            try:
                friend_list = FriendList.objects.get(user=this_user)
            except FriendList.DoesNotExist:
                return HttpResponse(f"No se pudo encontrar una lista de amigos para {this_user.username}")
            
            if user != this_user:
                if not user in friend_list.friends.all():
                    return HttpResponse("Debes ser amigo para ver su lista de amigos.")
            friends = []
            auth_user_friend_list = FriendList.objects.get(user=user)
            for friend in friend_list.friends.all():
                friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
            context['friends'] = friends
    else:		
        return HttpResponse("Debes ser amigo para ver su lista de amigos.")
    return render(request, "friend/friend_list.html", context)


def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        account = User.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("No puedes ver la solicitud de amistad de otro usuario.")
    else:
        redirect("login")
    return render(request, "friend/friend_requests.html", context)


def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("Ya le enviaste una solicitud de amistad.")
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Solicitud de amistad enviada."
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Solicitud de amistad enviada."
            
            if payload['response'] == None:
                payload['response'] = "Algo salió mal."
        else:
            payload['response'] = "No se puede enviar la solicitud de amistad"
    else:
        payload['response'] = "Debes estar autenticado para enviar una solicitud de amistad."
    return HttpResponse(json.dumps(payload), content_type="application/json")
    

def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request: 
                    friend_request.accept()
                    payload['response'] = "Solicitud de amistad aceptada."

                else:
                    payload['response'] = "Algo salió mal."
            else:
                payload['response'] = "Esta no es tu petición para aceptar."
        else:
            payload['response'] = "No se puede aceptar la solicitud de amistad."
    else:
        payload['response'] = "Debes estar autenticado para aceptar una solicitud de amistad."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Amigo eliminado con éxito."
            except Exception as e:
                payload['response'] = f"Algo salió mal: {str(e)}"
        else:
            payload['response'] = "Se produjo un error. No se pudo eliminar a ese amigo."
    else:
        payload['response'] = "Debes estar autenticado para eliminar a un amigo."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request: 
                    friend_request.decline()
                    payload['response'] = "Solicitud de amistad rechazada."
                else:
                    payload['response'] = "Algo salió mal."
            else:
                payload['response'] = "Esta no es una solicitud de amistad que puedas rechazar."
        else:
            payload['response'] = "No se puede rechazar la solicitud de amistad."
    else:
        payload['response'] = "Debes estar autenticado para rechazar una solicitud de amistad."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = User.objects.get(pk=user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
			except FriendRequest.DoesNotExist:
				payload['response'] = "No hay nada que cancelar. La solicitud de amistad no existe."

			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cancel()
				payload['response'] = "Solicitud de amistad cancelada."
			else:
				friend_requests.first().cancel()
				payload['response'] = "Solicitud de amistad cancelada."
		else:
			payload['response'] = "No se puede cancelar la solicitud de amistad."
	else:
		payload['response'] = "Debes estar autenticado para cancelar una solicitud de amistad."
	return HttpResponse(json.dumps(payload), content_type="application/json")