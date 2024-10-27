from django.db import models  # Importa el módulo models de Django
from django.utils import timezone  # Importa timezone para manejar fechas y horas
from django.contrib.auth.models import User  # Importa el modelo User de Django
from django.urls import reverse  # Importa reverse para crear URLs
from ckeditor.fields import RichTextField  # Importa RichTextField para contenido enriquecido

""" Modelo de publicación """
class Post(models.Model):
    title = models.CharField(max_length=150)  # Título de la publicación con un máximo de 150 caracteres
    content = RichTextField(blank=True, null=True)  # Contenido enriquecido, puede estar en blanco o ser nulo
    date_posted = models.DateTimeField(default=timezone.now)  # Fecha y hora de publicación, por defecto es ahora
    date_updated = models.DateTimeField(auto_now=True)  # Fecha y hora de la última actualización, se actualiza automáticamente
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User, elimina publicaciones si se elimina el usuario
    likes = models.ManyToManyField(User, related_name="blogpost", blank=True)  # Usuarios que han dado 'me gusta' a la publicación
    saves = models.ManyToManyField(User, related_name="blogsave", blank=True)  # Usuarios que han guardado la publicación

    def total_likes(self):
        return self.likes.count()  # Devuelve el total de 'me gusta'

    def total_saves(self):
        return self.saves.count()  # Devuelve el total de guardados

    def __str__(self):
        return self.title  # Devuelve el título como representación en cadena del objeto

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk":self.pk})  # Devuelve la URL absoluta de la publicación


""" Modelo de comentario """
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)  # Relación con el modelo Post, elimina comentarios si se elimina la publicación
    name = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User, elimina comentarios si se elimina el usuario
    body = models.TextField(max_length=200)  # Cuerpo del comentario con un máximo de 200 caracteres
    date_added = models.DateTimeField(auto_now_add=True)  # Fecha y hora en que se añadió el comentario
    likes = models.ManyToManyField(User, related_name="blogcomment", blank=True)  # Usuarios que han dado 'me gusta' al comentario
    reply = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE)  # Respuesta a otro comentario, puede ser nula

    def total_clikes(self):
        return self.likes.count()  # Devuelve el total de 'me gusta' en el comentario

    def __str__(self):
        return '%s - %s - %s' % (self.post.title, self.name, self.id)  # Devuelve una representación en cadena del comentario

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk":self.pk})  # Devuelve la URL absoluta de la publicación asociada
