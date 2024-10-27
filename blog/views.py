from notification.models import Notification  # Importa el modelo de notificación para manejar las notificaciones del sistema.
from django.core.checks import messages  # Importa mensajes de comprobación de Django, aunque no se utiliza aquí.
from django.shortcuts import render, get_object_or_404, redirect  # Funciones de ayuda para renderizar vistas y redirigir.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Mixins para restringir el acceso basado en la autenticación.
from django.contrib.auth.models import User  # Importa el modelo de usuario para manejar usuarios del sistema.
from django.urls import reverse_lazy, reverse  # Funciones para generar URLs dentro de la aplicación.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # Importa vistas genéricas para operaciones CRUD.
from .models import Comment, Post  # Importa los modelos de comentario y publicación.
from .forms import CommentForm  # Importa el formulario de comentario.
from django.http import HttpResponseRedirect, JsonResponse  # Clases para manejar respuestas HTTP.
from users.models import Profile  # Importa el modelo de perfil de usuario.
from itertools import chain  # Función para combinar iterables.
from django.contrib.auth.decorators import login_required  # Decorador para restringir el acceso a vistas a usuarios autenticados.
from django.contrib import messages  # Importa el sistema de mensajes de Django para notificaciones.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Importa las clases para paginación de resultados.
from django.template.loader import render_to_string  # Carga plantillas para renderizarlas como cadenas.
import random  # Importa el módulo random para generar valores aleatorios.
from blog.utils import is_ajax  # Importa la función para verificar si una solicitud es AJAX.


""" Página de inicio con todas las publicaciones """
def first(request):
    context = {
        'posts': Post.objects.all()  # Obtiene todas las publicaciones de la base de datos.
    }
    return render(request, 'blog/first.html', context)  # Renderiza la plantilla 'first.html' con el contexto de las publicaciones.


""" Publicaciones de los perfiles de usuario seguidos """
@login_required  # Asegura que solo los usuarios autenticados puedan acceder a esta vista.
def posts_of_following_profiles(request):
    profile = Profile.objects.get(user=request.user)  # Obtiene el perfil del usuario actual.
    users = [user for user in profile.following.all()]  # Crea una lista de usuarios que el perfil está siguiendo.
    posts = []  # Inicializa una lista para almacenar las publicaciones de los usuarios seguidos.
    qs = None  # Inicializa la variable de consulta a None.

    for u in users:  # Itera sobre cada usuario seguido.
        p = Profile.objects.get(user=u)  # Obtiene el perfil del usuario.
        p_posts = p.user.post_set.all()  # Obtiene todas las publicaciones de ese usuario.
        posts.append(p_posts)  # Agrega las publicaciones a la lista de publicaciones.

    my_posts = profile.profile_posts()  # Obtiene las publicaciones del propio perfil.
    posts.append(my_posts)  # Agrega las publicaciones del propio perfil a la lista de publicaciones.

    if len(posts) > 0:  # Verifica si hay publicaciones en la lista.
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)  # Combina y ordena las publicaciones por fecha de publicación de forma descendente.

    paginator = Paginator(qs, 5)  # Crea un paginador que muestra 5 publicaciones por página.
    page = request.GET.get('page')  # Obtiene el número de página de la solicitud.
    try:
        posts_list = paginator.page(page)  # Intenta obtener la lista de publicaciones de la página solicitada.
    except PageNotAnInteger:  # Maneja el caso en que la página no es un número entero.
        posts_list = paginator.page(1)  # Muestra la primera página si ocurre un error.
    except EmptyPage:  # Maneja el caso en que la página está fuera de rango.
        posts_list = paginator.page(paginator.num_pages)  # Muestra la última página si ocurre un error.

    return render(request, 'blog/feeds.html', {'profile': profile, 'posts': posts_list})  # Renderiza la plantilla 'feeds.html' con el perfil y las publicaciones paginadas.


""" Publicar Me gusta """
@login_required  # Decorador que asegura que el usuario esté autenticado.
def LikeView(request):
    # Obtiene el post basado en el ID proporcionado en la solicitud POST.
    post = get_object_or_404(Post, id=request.POST.get('id'))  
    liked = False  # Inicializa la variable liked como False.

    # Verifica si el usuario ya ha dado "me gusta" al post.
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Si ya le gusta, lo elimina de la lista de "me gusta".
        liked = False  # Actualiza liked a False.
        
        # Notificación de "me gusta" eliminada.
        notify = Notification.objects.filter(post=post, sender=request.user, notification_type=1)
        notify.delete()  # Elimina la notificación relacionada.

    else:
        post.likes.add(request.user)  # Si no le gusta, lo añade a la lista de "me gusta".
        liked = True  # Actualiza liked a True.
        
        # Crea una nueva notificación de "me gusta".
        notify = Notification(post=post, sender=request.user, user=post.author, notification_type=1)
        notify.save()  # Guarda la nueva notificación en la base de datos.

    # Contexto que incluye el post, total de "me gusta" y si el usuario ha dado "me gusta".
    context = {
        'post': post,
        'total_likes': post.total_likes(),  # Llama al método para obtener el total de "me gusta".
        'liked': liked,  # Incluye si le gusta o no.
    }

    # Verifica si la solicitud es una llamada AJAX.
    if is_ajax(request=request):
        # Renderiza la sección de "me gusta" en el HTML.
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})  # Devuelve la respuesta JSON con el HTML renderizado.


""" Guardar publicación """
@login_required  # Decorador que asegura que el usuario esté autenticado.
def SaveView(request):
    # Obtiene el post basado en el ID proporcionado en la solicitud POST.
    post = get_object_or_404(Post, id=request.POST.get('id'))  
    saved = False  # Inicializa la variable saved como False.

    # Verifica si el usuario ya ha guardado el post.
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)  # Si ya está guardado, lo elimina de la lista de guardados.
        saved = False  # Actualiza saved a False.
    else:
        post.saves.add(request.user)  # Si no está guardado, lo añade a la lista de guardados.
        saved = True  # Actualiza saved a True.

    # Contexto que incluye el post, total de guardados y si el usuario ha guardado el post.
    context = {
        'post': post,
        'total_saves': post.total_saves(),  # Llama al método para obtener el total de guardados.
        'saved': saved,  # Incluye si ha sido guardado o no.
    }

    # Verifica si la solicitud es una llamada AJAX.
    if is_ajax(request=request):
        # Renderiza la sección de "guardar" en el HTML.
        html = render_to_string('blog/save_section.html', context, request=request)
        return JsonResponse({'form': html})  # Devuelve la respuesta JSON con el HTML renderizado.


""" Comentarios en las publicaciones de me gusta """
@login_required  # Asegura que solo los usuarios autenticados puedan acceder a esta vista.
def LikeCommentView(request):  # Vista para manejar el "me gusta" en comentarios.
    # Obtiene el comentario basado en el ID proporcionado en la solicitud POST.
    post = get_object_or_404(Comment, id=request.POST.get('id'))  
    cliked = False  # Inicializa la variable cliked como False.

    # Verifica si el usuario ya ha dado "me gusta" al comentario.
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Si ya ha dado "me gusta", lo elimina.
        cliked = False  # Actualiza cliked a False.
    else:
        post.likes.add(request.user)  # Si no ha dado "me gusta", lo añade.
        cliked = True  # Actualiza cliked a True.

    # Obtiene el post relacionado basado en el ID proporcionado en la solicitud POST.
    cpost = get_object_or_404(Post, id=request.POST.get('pid'))
    
    # Obtiene todos los comentarios del post ordenados por ID de forma descendente.
    total_comments2 = cpost.comments.all().order_by('-id')
    total_comments = cpost.comments.filter(reply=None).order_by('-id')  # Comentarios que no son respuestas.

    tcl = {}  # Diccionario para almacenar el estado de "me gusta" de cada comentario.
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()  # Total de "me gusta" del comentario.
        cliked = False  # Inicializa el estado de "me gusta" del comentario.

        # Verifica si el usuario ha dado "me gusta" a este comentario.
        if cmt.likes.filter(id=request.user.id).exists():
            cliked = True  # Actualiza el estado si ha dado "me gusta".

        tcl[cmt.id] = cliked  # Almacena el estado en el diccionario.

    # Contexto que incluye el formulario de comentarios, el post, los comentarios y el estado de "me gusta".
    context = {
        'comment_form': CommentForm(),  # Crea un nuevo formulario de comentarios.
        'post': cpost,  # Post al que pertenece el comentario.
        'comments': total_comments,  # Comentarios del post.
        'total_clikes': post.total_clikes(),  # Total de "me gusta" del comentario.
        'clikes': tcl  # Estado de "me gusta" de cada comentario.
    }

    # Verifica si la solicitud es una llamada AJAX.
    if is_ajax(request=request):
        # Renderiza la sección de comentarios en el HTML.
        html = render_to_string('blog/comments.html', context, request=request)  
        return JsonResponse({'form': html})  # Devuelve la respuesta JSON con el HTML renderizado.


""" Página de inicio con todas las publicaciones """
class PostListView(ListView):
    model = Post  # Especifica el modelo a utilizar.
    template_name = 'blog/home.html'  # Define la plantilla a utilizar para renderizar la vista.
    context_object_name = 'posts'  # Nombre del contexto para acceder a los objetos en la plantilla.
    ordering = ['-date_posted']  # Ordena los posts por la fecha de publicación de forma descendente.
    paginate_by = 5  # Número de publicaciones por página para la paginación.

    def get_context_data(self, *args, **kwargs):
        # Obtiene el contexto de la clase base.
        context = super(PostListView, self).get_context_data()
        
        # Obtiene todos los usuarios excepto el usuario que ha iniciado sesión.
        users = list(User.objects.exclude(pk=self.request.user.pk))
        
        # Determina cuántos usuarios aleatorios seleccionar (máximo 3).
        if len(users) > 3:
            cnt = 3  # Si hay más de 3 usuarios, selecciona 3.
        else:
            cnt = len(users)  # De lo contrario, selecciona todos los usuarios disponibles.

        # Selecciona aleatoriamente un número definido de usuarios.
        random_users = random.sample(users, cnt)
        
        # Añade los usuarios aleatorios al contexto para la plantilla.
        context['random_users'] = random_users
        return context  # Retorna el contexto actualizado.


""" Todas las publicaciones de un usuario """
class UserPostListView(ListView):
    model = Post  # Especifica el modelo a utilizar.
    template_name = 'blog/user_posts.html'  # Define la plantilla a utilizar para renderizar la vista.
    context_object_name = 'posts'  # Nombre del contexto para acceder a los objetos en la plantilla.
    paginate_by = 5  # Número de publicaciones por página para la paginación.

    def get_queryset(self):
        # Obtiene el usuario basado en el nombre de usuario proporcionado en la URL.
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        # Filtra las publicaciones para incluir solo las del usuario especificado y las ordena por fecha de publicación de forma descendente.
        return Post.objects.filter(author=user).order_by('-date_posted')


""" Vista de los detalles de la publicación """
def PostDetailView(request, pk):
    # Obtiene la publicación basada en el identificador (pk) proporcionado. Si no se encuentra, devuelve un 404.
    stuff = get_object_or_404(Post, id=pk)

    # Obtiene el total de "me gusta", "guardados" y comentarios para la publicación.
    total_likes = stuff.total_likes()
    total_saves = stuff.total_saves()
    total_comments = stuff.comments.all().filter(reply=None).order_by('-id')  # Comentarios principales.
    total_comments2 = stuff.comments.all().order_by('-id')  # Todos los comentarios.

    context = {}

    # Maneja el envío de comentarios a través de una solicitud POST.
    if request.method == "POST":
        comment_qs = None
        comment_form = CommentForm(request.POST or None)  # Crea el formulario de comentarios con los datos enviados.
        if comment_form.is_valid():  # Verifica si el formulario es válido.
            form = request.POST.get('body')  # Obtiene el cuerpo del comentario.
            reply_id = request.POST.get('comment_id')  # Verifica si hay un comentario de respuesta.
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)  # Obtiene el comentario al que se está respondiendo.
            
            # Crea un nuevo comentario asociado a la publicación.
            comment = Comment.objects.create(name=request.user, post=stuff, body=form, reply=comment_qs)
            comment.save()  # Guarda el nuevo comentario.
            
            # Crea una notificación para el autor de la publicación.
            if reply_id:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form, notification_type=4)
                notify.save()  # Notificación para respuesta.
            else:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form, notification_type=3)
                notify.save()  # Notificación para nuevo comentario.
            
            # Actualiza el conteo de comentarios.
            total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
            total_comments2 = stuff.comments.all().order_by('-id')
    else:
        comment_form = CommentForm()  # Inicializa el formulario si no es una solicitud POST.
             
    # Crea un diccionario para almacenar si cada comentario ha sido "me gusta".
    tcl = {}
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()  # Total de "me gusta" del comentario.
        cliked = False
        if cmt.likes.filter(id=request.user.id).exists():  # Verifica si el usuario ha dado "me gusta".
            cliked = True

        tcl[cmt.id] = cliked  # Almacena el estado del "me gusta".

    context["clikes"] = tcl  # Agrega el estado de "me gusta" al contexto.

    # Verifica si el usuario ha dado "me gusta" a la publicación.
    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    context["total_likes"] = total_likes  # Total de "me gusta".
    context["liked"] = liked  # Estado del "me gusta".

    # Verifica si el usuario ha guardado la publicación.
    saved = False
    if stuff.saves.filter(id=request.user.id).exists():
        saved = True
    context["total_saves"] = total_saves  # Total de guardados.
    context["saved"] = saved  # Estado de guardado.

    context['comment_form'] = comment_form  # Agrega el formulario de comentarios al contexto.
    context['post'] = stuff  # Agrega la publicación al contexto.
    context['comments'] = total_comments  # Agrega los comentarios al contexto.

    # Maneja la respuesta AJAX.
    if is_ajax(request=request):
        html = render_to_string('blog/comments.html', context, request=request)  # Renderiza los comentarios para AJAX.
        return JsonResponse({'form': html})  # Devuelve el HTML renderizado en formato JSON.

    # Renderiza la plantilla de detalle de la publicación con el contexto.
    return render(request, 'blog/post_detail.html', context)


""" Crear publicación """
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  # Especifica que el modelo asociado a esta vista es Post (Modelo).
    fields = ['title', 'content']  # Campos que se mostrarán en el formulario de creación.

    def form_valid(self, form):
        # Asigna el autor de la publicación como el usuario que ha iniciado sesión.
        form.instance.author = self.request.user
        return super().form_valid(form)  # Llama al método de la clase base para procesar el formulario.


""" Actualizar publicación """
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  # Especifica que el modelo asociado a esta vista es Post.
    fields = ['title', 'content']  # Campos que se mostrarán en el formulario de actualización.

    def form_valid(self, form):
        # Asigna el autor de la publicación como el usuario que ha iniciado sesión.
        form.instance.author = self.request.user
        return super().form_valid(form)  # Llama al método de la clase base para procesar el formulario.

    def test_func(self):
        # Verifica si el usuario actual es el autor de la publicación antes de permitir la actualización.
        post = self.get_object()  # Obtiene el objeto de la publicación que se está actualizando.
        if self.request.user == post.author:
            return True  # Permite la actualización si el usuario es el autor.
        return False  # Deniega la actualización si el usuario no es el autor.


""" Borrar publicación """
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  # Especifica que el modelo asociado a esta vista es Post (Publicación).
    success_url = '/'  # URL a la que se redirige después de eliminar la publicación.

    def test_func(self):
        # Verifica si el usuario actual es el autor de la publicación antes de permitir la eliminación.
        post = self.get_object()  # Obtiene el objeto de la publicación que se va a eliminar.
        if self.request.user == post.author:
            return True  # Permite la eliminación si el usuario es el autor.
        return False  # Deniega la eliminación si el usuario no es el autor.


""" Acerca de la página """
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})


""" Buscar publicación por el título o usuario """
def search(request):
    query = request.GET['query']  # Obtiene la consulta de búsqueda del parámetro GET.
    
    # Verifica si la longitud de la consulta es válida.
    if len(query) >= 150 or len(query) < 1:
        allposts = Post.objects.none()  # Si la longitud es inválida, no se devuelve ninguna publicación.
    elif len(query.strip()) == 0:
        allposts = Post.objects.none()  # Si la consulta está vacía después de eliminar espacios, no se devuelve ninguna publicación.
    else:
        # Filtra las publicaciones que contienen la consulta en el título o que pertenecen al autor con el nombre de usuario coincidente.
        allpostsTitle = Post.objects.filter(title__icontains=query)  # Publicaciones que contienen el texto en el título.
        allpostsAuthor = Post.objects.filter(author__username=query)  # Publicaciones del autor que coincide con el nombre de usuario.
        allposts = allpostsAuthor.union(allpostsTitle)  # Combina los resultados en un solo queryset.
    
    params = {'allposts': allposts}  # Crea un diccionario de parámetros para pasar a la plantilla.
    return render(request, 'blog/search_results.html', params)  # Renderiza la plantilla con los resultados de búsqueda.


""" Publicaciones que le gustan a un usuario """
@login_required
def AllLikeView(request):
    user = request.user  # Obtiene el usuario actualmente autenticado.
    liked_posts = user.blogpost.all()  # Recupera todas las publicaciones que le gustan al usuario.
    context = {
        'liked_posts': liked_posts  # Crea un contexto con las publicaciones que le gustan.
    }
    return render(request, 'blog/liked_posts.html', context)  # Renderiza la plantilla con el contexto.


""" Publicaciones guardadas por un usuario """
@login_required
def AllSaveView(request):
    user = request.user  # Obtiene el usuario actualmente autenticado.
    saved_posts = user.blogsave.all()  # Recupera todas las publicaciones que el usuario ha guardado.
    context = {
        'saved_posts': saved_posts  # Crea un contexto con las publicaciones guardadas.
    }
    return render(request, 'blog/saved_posts.html', context)  # Renderiza la plantilla con el contexto.
