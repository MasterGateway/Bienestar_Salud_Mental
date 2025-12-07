"""
CAPA DE PRESENTACIÓN - Formularios
Validación de entrada de datos del usuario
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..data.models import CustomUser, Lugar, Evento


class CustomUserCreationForm(UserCreationForm):
    """Formulario de registro de usuario"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }


class LugarForm(forms.ModelForm):
    """Formulario para crear/editar lugares"""
    
    class Meta:
        model = Lugar
        fields = ['nombre', 'descripcion', 'direccion', 'latitud', 'longitud', 'url_mapa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Biblioteca Central UNAS'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del lugar...'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Campus UNAS, Tingo María'
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ej: -9.300000'
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ej: -75.900000'
            }),
            'url_mapa': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://maps.google.com/...'
            })
        }
        labels = {
            'nombre': 'Nombre del Lugar',
            'descripcion': 'Descripción',
            'direccion': 'Dirección',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'url_mapa': 'URL del Mapa (opcional)'
        }
    
    def clean_latitud(self):
        """Validación de latitud"""
        latitud = self.cleaned_data.get('latitud')
        if latitud and not (-90 <= latitud <= 90):
            raise forms.ValidationError("La latitud debe estar entre -90 y 90")
        return latitud
    
    def clean_longitud(self):
        """Validación de longitud"""
        longitud = self.cleaned_data.get('longitud')
        if longitud and not (-180 <= longitud <= 180):
            raise forms.ValidationError("La longitud debe estar entre -180 y 180")
        return longitud


class EventoForm(forms.ModelForm):
    """Formulario para crear/editar eventos"""
    
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'lugar', 'capacidad_maxima']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Taller de Meditación'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del evento...'
            }),
            'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_fin': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'lugar': forms.Select(attrs={
                'class': 'form-control'
            }),
            'capacidad_maxima': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej: 20'
            })
        }
        labels = {
            'titulo': 'Título del Evento',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha y Hora de Inicio',
            'fecha_fin': 'Fecha y Hora de Fin',
            'lugar': 'Lugar',
            'capacidad_maxima': 'Capacidad Máxima'
        }


class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar perfil de usuario"""
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'telefono']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
