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

class RegistroAdminFormulario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'rol', 'password']
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
            'rol': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Rol',
                'id': 'rol'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'id': 'password'
            })
        }

class ProductoAdminFormulario(forms.ModelForm):
    class Meta:
        model = Producto
        fields =  ['nombre', 'precio', 'tipo', 'ingredientes']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de Producto',
                'id': 'nombre'
            }),
            'precio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio (Ej. 0.00)',
                'id': 'precio'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo',
                'id': 'tipo'
            }),
            'ingredientes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingredientes',
                'id': 'ingredientes'
            }),
        }

class MesaAdminFormulario(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numero de Mesa',
                'id': 'numero'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Estado',
                'id': 'estado'
            })
        }

class PersonalizarForm(forms.ModelForm):
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
