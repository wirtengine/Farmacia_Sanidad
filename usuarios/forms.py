from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    
    # Usa los mismos roles que definiste en el modelo
    rol = forms.ChoiceField(choices=Usuario.ROLES, required=True, label='Rol')

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'password1', 'password2']