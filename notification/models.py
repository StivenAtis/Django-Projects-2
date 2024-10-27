# Importación de módulos necesarios para la definición de modelos en Django.
from django.db import models
from django.contrib.auth.models import User  # Importación del modelo de usuario de Django.

# Definición del modelo de Notificación.
class Notification(models.Model):
    # Tipos de notificación como tuplas.
    NOTIFICATION_TYPES = (
        (1, 'Like'),           # Notificación de "Me gusta".
        (2, 'Follow'),         # Notificación de "Seguir".
        (3, 'Comment'),        # Notificación de "Comentario".
        (4, 'Reply'),          # Notificación de "Respuesta".
        (5, 'Like-Comment'),   # Notificación de "Me gusta en comentario".
        (6, 'Like-Reply'),     # Notificación de "Me gusta en respuesta".
    )

    # Relación con el modelo Post, permite a las notificaciones estar asociadas a publicaciones específicas.
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='notify_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_from_user')  # Usuario que envía la notificación.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_to_user')        # Usuario que recibe la notificación.
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)  # Tipo de notificación.
    text_preview = models.CharField(max_length=120, blank=True)          # Texto de vista previa de la notificación.
    date = models.DateTimeField(auto_now_add=True)                       # Fecha de creación de la notificación, se establece automáticamente.
    is_seen = models.BooleanField(default=False)                          # Indica si la notificación ha sido vista.

    # Representación en cadena del modelo, útil para depuración y administración.
    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.id, self.post, self.sender, self.user, self.notification_type)
