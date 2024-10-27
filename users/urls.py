from django.urls import path  # Importación del módulo path para definir las URL.
from . import views  # Importación de las vistas definidas en el módulo actual.

urlpatterns = [
    path('all/', views.ProfileListView.as_view(), name='profile-list-view'),  # Ruta para listar todos los perfiles.
    path('follow/', views.follow_unfollow_profile, name='follow-unfollow-view'),  # Ruta para seguir o dejar de seguir un perfil.
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),  # Ruta para ver los detalles de un perfil específico.
    path('public-profile/<str:username>/', views.public_profile, name='public-profile'),  # Ruta para ver el perfil público de un usuario por su nombre de usuario.
]
