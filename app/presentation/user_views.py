"""
CAPA DE PRESENTACIÓN - Views de Usuarios (Admin)
SOLO maneja HTTP - La lógica está en UserLogic
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from ..business.user_logic import UserLogic
from .forms import UserUpdateForm


def es_staff(user):
    """Verificar si el usuario es staff"""
    return user.is_staff


@login_required
@user_passes_test(es_staff)
def lista_usuarios(request):
    """Vista para listar usuarios (solo admin)"""
    # Obtener parámetro de búsqueda
    query = request.GET.get('q', '')
    
    # Llamar a la CAPA DE NEGOCIO
    if query:
        usuarios = UserLogic.buscar(query)
    else:
        usuarios = UserLogic.obtener_todos()
    
    # Paginación
    paginator = Paginator(usuarios, 20)  # 20 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'total_usuarios': usuarios.count()
    }
    
    return render(request, 'usuarios/lista.html', context)


@login_required
def perfil_usuario(request):
    """Vista para ver/editar perfil del usuario actual"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            # Llamar a la CAPA DE NEGOCIO
            resultado = UserLogic.actualizar(
                user_id=request.user.id,
                email=form.cleaned_data.get('email'),
                bio=form.cleaned_data.get('bio'),
                telefono=form.cleaned_data.get('telefono')
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
                return redirect('perfil_usuario')
            else:
                messages.error(request, resultado['mensaje'])
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'usuarios/perfil.html', {'form': form})


@login_required
@user_passes_test(es_staff)
def editar_usuario(request, user_id):
    """Vista para editar un usuario (solo admin)"""
    # Obtener usuario
    resultado = UserLogic.obtener_por_id(user_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
        return redirect('lista_usuarios')
    
    usuario = resultado['user']
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=usuario)
        
        if form.is_valid():
            # Llamar a la CAPA DE NEGOCIO
            resultado = UserLogic.actualizar(
                user_id=user_id,
                email=form.cleaned_data.get('email'),
                bio=form.cleaned_data.get('bio'),
                telefono=form.cleaned_data.get('telefono'),
                is_active=form.cleaned_data.get('is_active')
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
                return redirect('lista_usuarios')
            else:
                messages.error(request, resultado['mensaje'])
    else:
        form = UserUpdateForm(instance=usuario)
    
    return render(request, 'usuarios/editar.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
@user_passes_test(es_staff)
def eliminar_usuario(request, user_id):
    """Vista para eliminar un usuario (solo admin)"""
    if request.method == 'POST':
        # Verificar que no se elimine a sí mismo
        if user_id == request.user.id:
            messages.error(request, "No puedes eliminar tu propia cuenta")
            return redirect('lista_usuarios')
        
        # Llamar a la CAPA DE NEGOCIO
        resultado = UserLogic.eliminar(user_id, permanente=False)
        
        if resultado['exito']:
            messages.success(request, resultado['mensaje'])
        else:
            messages.error(request, resultado['mensaje'])
        
        return redirect('lista_usuarios')
    
    # GET: Mostrar confirmación
    resultado = UserLogic.obtener_por_id(user_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
        return redirect('lista_usuarios')
    
    return render(request, 'usuarios/eliminar.html', {
        'usuario': resultado['user']
    })


@login_required
def detalle_usuario(request, user_id):
    """Vista para ver detalle de un usuario"""
    resultado = UserLogic.obtener_por_id(user_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
        return redirect('lista_usuarios')
    
    usuario = resultado['user']
    
    # Obtener estadísticas del usuario
    estadisticas = UserLogic.obtener_estadisticas(user_id)
    
    context = {
        'usuario': usuario,
        'estadisticas': estadisticas
    }
    
    return render(request, 'usuarios/detalle.html', context)
