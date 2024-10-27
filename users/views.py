from friend.models import FriendList, FriendRequest  # Importación de modelos para manejar la lista de amigos y solicitudes de amistad.
from django.shortcuts import render, redirect  # Importación de funciones para renderizar y redirigir vistas.
from django.contrib.auth.decorators import login_required  # Decorador para requerir autenticación de usuario.
from django.contrib import messages  # Importación del sistema de mensajes de Django.
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm  # Importación de formularios para el registro y actualización de usuarios y perfiles.
from .models import Profile  # Importación del modelo Profile.
from django.contrib.auth.models import User  # Importación del modelo User.
from django.views.generic import ListView, DetailView  # Importación de vistas genéricas para listar y detallar.
from django.contrib.auth.mixins import LoginRequiredMixin  # Mezcla para requerir autenticación en vistas basadas en clases.
from django.dispatch import receiver  # Decorador para conectar señales con funciones.
from django.contrib.auth.signals import user_logged_in, user_logged_out  # Señales para eventos de inicio y cierre de sesión.
from notification.models import Notification  # Importación del modelo Notification.
import requests  # Importación de requests para manejar solicitudes HTTP.
from django.conf import settings  # Importación de configuraciones del proyecto.
from friend.utils import get_friend_request_or_false  # Importación de utilidad para manejar solicitudes de amistad.
from friend.friend_request_status import FriendRequestStatus  # Importación de constantes para estados de solicitud de amistad.


# Señal que se activa cuando un usuario inicia sesión.
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.profile.is_online = True  # Marcar al usuario como en línea.
    user.profile.save()  # Guardar los cambios en el perfil del usuario.


# Señal que se activa cuando un usuario cierra sesión.
@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.profile.is_online = False  # Marcar al usuario como fuera de línea.
    user.profile.save()  # Guardar los cambios en el perfil del usuario.


""" Seguir y dejar de seguir usuarios """
@login_required  # Requiere que el usuario esté autenticado para acceder a la función.
def follow_unfollow_profile(request):
    if request.method == 'POST':  # Verifica que la solicitud sea de tipo POST.
        my_profile = Profile.objects.get(user=request.user)  # Obtiene el perfil del usuario actual.
        pk = request.POST.get('profile_pk')  # Obtiene el ID del perfil que se va a seguir/dejar de seguir.
        obj = Profile.objects.get(pk=pk)  # Obtiene el perfil objetivo.

        if obj.user in my_profile.following.all():  # Si el usuario objetivo ya está siendo seguido.
            my_profile.following.remove(obj.user)  # Se deja de seguir al usuario.
            notify = Notification.objects.filter(sender=request.user, notification_type=2)  # Busca notificaciones de seguimiento.
            notify.delete()  # Elimina la notificación de seguimiento.
        else:  # Si el usuario objetivo no está siendo seguido.
            my_profile.following.add(obj.user)  # Se sigue al usuario.
            notify = Notification(sender=request.user, user=obj.user, notification_type=2)  # Crea una nueva notificación de seguimiento.
            notify.save()  # Guarda la notificación.

        return redirect(request.META.get('HTTP_REFERER'))  # Redirige a la página anterior.
    
    return redirect('profile-list-view')  # Si no es una solicitud POST, redirige a la vista de lista de perfiles.


""" Creación de una cuenta de usuario """
def register(request):
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST.
        form = UserRegisterForm(request.POST)  # Crea un formulario de registro con los datos enviados.
        if form.is_valid():  # Verifica si el formulario es válido.

            # reCAPTCHA V2 (comentado por ahora)
            # recaptcha_response = request.POST.get('g-recaptcha-response')  # Obtiene la respuesta de reCAPTCHA del formulario.
            # data = {  # Prepara los datos para la verificación de reCAPTCHA.
            #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            #     'response': recaptcha_response
            # }
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)  # Envía una solicitud a la API de reCAPTCHA.
            # result = r.json()  # Obtiene el resultado de la verificación.

            # if result['success']:  # Si la verificación fue exitosa.
                form.save()  # Guarda el nuevo usuario en la base de datos.
                username = form.cleaned_data.get('username')  # Obtiene el nombre de usuario del formulario.
                messages.success(request, f"¡Tu cuenta ha sido creada! Puedes iniciar sesión ahora")  # Envía un mensaje de éxito.
                return redirect('login')  # Redirige al usuario a la página de inicio de sesión.
            # else:  # Si la verificación de reCAPTCHA falló.
            #     messages.error(request, 'Invalid reCAPTCHA. Please try again.')  # Envía un mensaje de error.
            
    else:
        form = UserRegisterForm()  # Si no es una solicitud POST, crea un nuevo formulario vacío.
    return render(request, 'users/register.html', {'form': form})  # Renderiza la plantilla de registro con el formulario.


""" Perfil del usuario (Actualización) """
@login_required  # Asegura que solo los usuarios autenticados puedan acceder a esta vista.
def profile(request):
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST.
        u_form = UserUpdateForm(request.POST, instance=request.user)  # Crea un formulario para actualizar el usuario.
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  # Crea un formulario para actualizar el perfil.

        if u_form.is_valid() and p_form.is_valid():  # Verifica si ambos formularios son válidos.
            u_form.save()  # Guarda los cambios en el usuario.
            p_form.save()  # Guarda los cambios en el perfil.
            messages.success(request, f"¡Tu cuenta ha sido actualizada!")  # Envía un mensaje de éxito al usuario.
            return redirect('profile')  # Redirige al usuario a la página de su perfil.
    else:
        u_form = UserUpdateForm(instance=request.user)  # Crea un formulario vacío para actualizar el usuario con los datos actuales.
        p_form = ProfileUpdateForm(instance=request.user.profile)  # Crea un formulario vacío para actualizar el perfil con los datos actuales.
    
    context = {
        'u_form': u_form,  # Agrega el formulario de usuario al contexto.
        'p_form': p_form   # Agrega el formulario de perfil al contexto.
    }

    return render(request, 'users/profile.html', context)  # Renderiza la plantilla de perfil con los formularios.


""" Crear una vista de perfil pública """
def public_profile(request, username):
    user = User.objects.get(username=username)  # Obtiene el objeto User basado en el nombre de usuario proporcionado.
    return render(request, 'users/public_profile.html', {"cuser": user})  # Renderiza la plantilla de perfil público, pasando el usuario como contexto.


""" Todos los perfiles de usuario """
class ProfileListView(LoginRequiredMixin, ListView):  # Vista de lista de perfiles, requiere inicio de sesión.
    model = Profile  # Modelo que se utilizará para esta vista.
    template_name = "users/all_profiles.html"  # Nombre de la plantilla que se usará para renderizar.
    context_object_name = "profiles"  # Nombre del contexto que se pasará a la plantilla.

    def get_queryset(self):  # Método que define la consulta para obtener los perfiles.
        return Profile.objects.all().exclude(user=self.request.user)  # Devuelve todos los perfiles excluyendo el del usuario actual.


""" Vista detallada del perfil de usuario """
class ProfileDetailView(LoginRequiredMixin, DetailView):  # Vista detallada que requiere inicio de sesión.
    model = Profile  # Modelo de la vista.
    template_name = "users/user_profile_details.html"  # Plantilla utilizada para renderizar la vista.
    context_object_name = "profiles"  # Nombre del contexto para la plantilla.

    def get_queryset(self):  # Método para obtener el conjunto de consultas.
        return Profile.objects.all().exclude(user=self.request.user)  # Excluye el perfil del usuario actual.

    def get_object(self, **kwargs):  # Método para obtener el objeto de perfil específico.
        pk = self.kwargs.get("pk")  # Obtiene el valor de pk de los argumentos de la URL.
        view_profile = Profile.objects.get(pk=pk)  # Recupera el perfil correspondiente.
        return view_profile  # Devuelve el perfil.

    def get_context_data(self, **kwargs):  # Método para agregar datos adicionales al contexto.
        context = super().get_context_data(**kwargs)  # Obtiene el contexto de la clase padre.
        view_profile = self.get_object()  # Obtiene el perfil que se está viendo.
        my_profile = Profile.objects.get(user=self.request.user)  # Obtiene el perfil del usuario actual.
        
        # Verifica si el perfil visto está en la lista de seguidores del usuario actual.
        context["follow"] = view_profile.user in my_profile.following.all()

        # FRIENDS START

        account = view_profile.user  # Usuario cuyo perfil se está viendo.
        try:
            friend_list = FriendList.objects.get(user=account)  # Intenta obtener la lista de amigos.
        except FriendList.DoesNotExist:  # Si no existe, crea una nueva.
            friend_list = FriendList(user=account)
            friend_list.save()
        
        friends = friend_list.friends.all()  # Obtiene todos los amigos de la lista.
        context['friends'] = friends  # Añade los amigos al contexto.

        # Variables de estado para la relación del usuario actual con el perfil visto.
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests = None
        user = self.request.user

        if user.is_authenticated and user != account:  # Verifica si el usuario está autenticado y no es el mismo.
            is_self = False
            is_friend = friends.filter(pk=user.id).exists()  # Verifica si son amigos.
            # Verifica el estado de las solicitudes de amistad.
            if get_friend_request_or_false(sender=account, receiver=user) != False:
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).pk
            elif get_friend_request_or_false(sender=user, receiver=account) != False:
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
        
        elif not user.is_authenticated:  # Si no está autenticado, se establece como falso.
            is_self = False
        
        else:  # Si es el mismo usuario, intenta obtener las solicitudes de amistad.
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
        
        # Añade el estado de la relación al contexto.
        context['request_sent'] = request_sent
        context['is_friend'] = is_friend
        context['is_self'] = is_self
        context['friend_requests'] = friend_requests  # Añade las solicitudes de amistad al contexto.

        # FRIENDS END
        
        return context  # Devuelve el contexto con los datos adicionales.
