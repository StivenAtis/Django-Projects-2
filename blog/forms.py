from django import forms  # Importa el módulo forms de Django
from django.forms import fields, widgets  # Importa fields y widgets del módulo forms
from .models import Post, Comment  # Importa los modelos Post y Comment desde el módulo actual

class CommentForm(forms.ModelForm):  # Define la clase CommentForm que hereda de ModelForm
    # Define un campo 'body' como un área de texto
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control custom-txt','cols':'40','rows':'3'}),  # Personaliza el widget con clases CSS y atributos
        label=''  # Sin etiqueta para este campo
    )

    class Meta:  # Clase interna Meta para configurar el formulario
        model = Comment  # Especifica el modelo asociado al formulario
        fields = ['body',]  # Define los campos que se incluirán en el formulario