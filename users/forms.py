# Importación de módulos necesarios para crear formularios en Django.
from django import forms
from django.contrib.auth.models import User  # Modelo de usuario de Django.
from django.contrib.auth.forms import UserCreationForm  # Formulario de creación de usuario.
from .models import Profile  # Importación del modelo Profile.
from PIL import Image  # Biblioteca para manipulación de imágenes.

# Formulario para el registro de nuevos usuarios.
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Campo de email adicional.

    class Meta:
        model = User  # Modelo base del formulario.
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']  # Campos del formulario.

# Formulario para actualizar información del usuario.
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # Campo de email.

    class Meta:
        model = User  # Modelo base del formulario.
        fields = ['first_name', 'last_name', 'username', 'email']  # Campos del formulario.

# Formulario para actualizar el perfil del usuario.
class ProfileUpdateForm(forms.ModelForm):
    # Campos ocultos para manejar coordenadas y dimensiones para la imagen.
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    # Campo para la imagen de perfil, con validación de tipo de archivo.
    image = forms.ImageField(label=('Image'), error_messages={'invalid': ("Image files only")}, widget=forms.FileInput, required=False)

    class Meta:
        model = Profile  # Modelo base del formulario.
        fields = ['bio', 'date_of_birth', 'image']  # Campos del formulario.

    """ Guardar imagen recortada """
    def save(self, *args, **kwargs):
        img = super(ProfileUpdateForm, self).save(*args, **kwargs)  # Llama al método save del modelo.

        # Obtiene las coordenadas y dimensiones para el recorte.
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        # Si hay valores para recortar, procesa la imagen.
        if x and y and w and h:
            image = Image.open(img.image)  # Abre la imagen original.
            cropped_image = image.crop((x, y, w + x, h + y))  # Recorta la imagen.
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)  # Redimensiona la imagen.
            resized_image.save(img.image.path)  # Guarda la imagen recortada en la ruta original.

        return img  # Devuelve la instancia del modelo guardada.