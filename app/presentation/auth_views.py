"""
CAPA DE PRESENTACIÓN - Views de Autenticación
SOLO maneja HTTP requests/responses
La lógica está en la capa de negocio
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from ..business.user_logic import UserLogic
from .forms import CustomUserCreationForm


def login_view(request):
    """Vista de inicio de sesión"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Llamar a la CAPA DE NEGOCIO
        resultado = UserLogic.autenticar(username, password)
        
        if resultado['exito']:
            login(request, resultado['user'])
            messages.success(request, f'Bienvenido {username}!')
            return redirect('home')
        else:
            messages.error(request, resultado['mensaje'])
    
    # Usar el template del proyecto original
    return render(request, 'app/login.html')


def register_view(request):
    """Vista de registro"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            # Llamar a la CAPA DE NEGOCIO
            resultado = UserLogic.registrar(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                password_confirm=form.cleaned_data['password2']
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
                return redirect('login')
            else:
                messages.error(request, resultado['mensaje'])
    else:
        form = CustomUserCreationForm()
    
    # Usar el template del proyecto original
    return render(request, 'app/register.html', {'form': form})


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login')


def nueva_pagina_view(request):
    """Vista de página de inicio (pública)"""
    return render(request, 'app/inicio.html')


@login_required
def home_view(request):
    """Vista de página principal"""
    # Usar el template del proyecto original
    return render(request, 'app/home.html')


def contact_view(request):
    """Vista de contacto"""
    if request.method == 'POST':
        try:
            from django.core.exceptions import ValidationError
            from django.core.validators import validate_email
            
            # Captura los datos del formulario
            name = request.POST.get('name')
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            
            # Validación de campos vacíos
            if not name or not email or not message:
                raise ValidationError("Los campos Nombre, Email y Mensaje son obligatorios.")
            
            # Validación de email
            validate_email(email)
            
            # Simulación de procesamiento exitoso
            print(f"Contacto recibido de {name} ({email}): {message}")
            
            messages.success(request, '¡Gracias por contactarnos! Te responderemos pronto.')
            return render(request, 'app/contact.html', {'name': name})
        
        except ValidationError as e:
            messages.error(request, f'Error de validación: {e}')
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado: {e}')
    
    return render(request, 'app/contact.html')
