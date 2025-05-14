from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class RegistroFormulario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'nombre' ,'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo',
                'id': 'email'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de Usuario',
                'id': 'nombre'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'id': 'password'
            })
        }

class LoginFormulario(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginFormulario, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo',
            'id': 'email'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'password'
        })