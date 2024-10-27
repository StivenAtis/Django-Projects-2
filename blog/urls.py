from django.urls import path  # Importa el módulo path para definir las rutas de la aplicación
from . import views  # Importa las vistas del módulo actual
from .views import (
    AllSaveView, 
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView, 
    SaveView, 
    UserPostListView, 
    LikeView, 
    LikeCommentView, 
    posts_of_following_profiles,  
    AllLikeView
)

urlpatterns = [
    path('', views.first, name='firsthome'),  # Ruta para la página principal
    path('home/', PostListView.as_view(), name='blog-home'),  # Ruta para la lista de publicaciones
    path('feed/', posts_of_following_profiles, name='posts-follow-view'),  # Ruta para ver publicaciones de perfiles seguidos
    path('post/user/<str:username>/', UserPostListView.as_view(), name='user-posts'),  # Ruta para publicaciones de un usuario específico
    path('post/<int:pk>/', PostDetailView, name='post-detail'),  # Ruta para los detalles de una publicación
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Ruta para actualizar una publicación
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Ruta para eliminar una publicación
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Ruta para crear una nueva publicación
    path('post/like/', LikeView, name='post-like'),  # Ruta para dar 'me gusta' a una publicación
    path('liked-posts/', AllLikeView, name='all-like'),  # Ruta para ver todas las publicaciones que han recibido 'me gusta'
    path('post/save/', SaveView, name='post-save'),  # Ruta para guardar una publicación
    path('saved-posts/', AllSaveView, name='all-save'),  # Ruta para ver todas las publicaciones guardadas
    path('post/comment/like/', LikeCommentView, name='comment-like'),  # Ruta para dar 'me gusta' a un comentario
    path('about/', views.about, name='blog-about'),  # Ruta para la página 'Acerca de'
    path('search/', views.search, name='search'),  # Ruta para la búsqueda de publicaciones
]