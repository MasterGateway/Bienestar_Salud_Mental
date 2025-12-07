"""
CAPA DE PRESENTACIÓN - Views de Eventos
SOLO maneja HTTP - La lógica está en EventoLogic
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ..business.evento_logic import EventoLogic
from .forms import EventoForm


@login_required
def lista_eventos(request):
    """Vista para listar eventos activos"""
    # Obtener parámetros
    query = request.GET.get('q', '')
    filtro = request.GET.get('filtro', 'todos')  # todos, proximos, disponibles
    
    # Llamar a la CAPA DE NEGOCIO
    if query:
        eventos = EventoLogic.buscar(query)
    else:
        if filtro == 'proximos':
            eventos = EventoLogic.obtener_proximos()
        elif filtro == 'disponibles':
            eventos = EventoLogic.obtener_disponibles()
        else:
            eventos = EventoLogic.obtener_todos()
    
    # Paginación
    paginator = Paginator(eventos, 12)  # 12 eventos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'filtro': filtro,
        'total_eventos': eventos.count()
    }
    
    # Usar el template del proyecto original
    return render(request, 'app/eventos.html', context)


@login_required
def crear_evento(request):
    """Vista para crear un evento"""
    if request.method == 'POST':
        form = EventoForm(request.POST)
        
        if form.is_valid():
            # Llamar a la CAPA DE NEGOCIO
            resultado = EventoLogic.crear(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
                fecha_inicio=form.cleaned_data['fecha_inicio'],
                fecha_fin=form.cleaned_data['fecha_fin'],
                lugar_id=form.cleaned_data['lugar'].id,
                capacidad_maxima=form.cleaned_data['capacidad_maxima']
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
                return redirect('eventos')
            else:
                messages.error(request, resultado['mensaje'])
    else:
        form = EventoForm()
    
    # Mostrar formulario en la misma página de eventos
    return redirect('eventos')


@login_required
def detalle_evento(request, evento_id):
    """Vista para ver detalle de un evento"""
    resultado = EventoLogic.obtener_por_id(evento_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
        return redirect('eventos')
    
    evento = resultado['evento']
    usuario_inscrito = request.user in evento.inscritos.all()
    
    context = {
        'evento': evento,
        'usuario_inscrito': usuario_inscrito,
        'plazas_disponibles': evento.plazas_disponibles,
        'esta_lleno': evento.esta_lleno
    }
    
    # Redirigir a eventos por ahora (puedes crear template específico después)
    return redirect('eventos')


@login_required
def inscribir_evento(request, evento_id):
    """Vista para inscribirse a un evento"""
    if request.method == 'POST':
        # Llamar a la CAPA DE NEGOCIO
        resultado = EventoLogic.inscribir_usuario(
            evento_id=evento_id,
            user_id=request.user.id
        )
        
        if resultado['exito']:
            messages.success(request, resultado['mensaje'])
        else:
            messages.error(request, resultado['mensaje'])
    
    return redirect('eventos')


@login_required
def desinscribir_evento(request, evento_id):
    """Vista para desinscribirse de un evento"""
    if request.method == 'POST':
        # Llamar a la CAPA DE NEGOCIO
        resultado = EventoLogic.desinscribir_usuario(
            evento_id=evento_id,
            user_id=request.user.id
        )
        
        if resultado['exito']:
            messages.success(request, resultado['mensaje'])
        else:
            messages.error(request, resultado['mensaje'])
    
    return redirect('eventos')


@login_required
def mis_eventos(request):
    """Vista para ver eventos del usuario actual"""
    # Llamar a la CAPA DE NEGOCIO
    eventos = EventoLogic.obtener_por_usuario(request.user.id)
    
    # Paginación
    paginator = Paginator(eventos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_eventos': eventos.count()
    }
    
    # Usar el mismo template de eventos
    return render(request, 'app/eventos.html', context)


@login_required
def editar_evento(request, evento_id):
    """Vista para editar un evento"""
    resultado = EventoLogic.obtener_por_id(evento_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
        return redirect('eventos')
    
    evento = resultado['evento']
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        
        if form.is_valid():
            # Llamar a la CAPA DE NEGOCIO
            resultado = EventoLogic.actualizar(
                evento_id=evento_id,
                **form.cleaned_data
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
            else:
                messages.error(request, resultado['mensaje'])
    
    return redirect('eventos')


@login_required
def eliminar_evento(request, evento_id):
    """Vista para eliminar un evento"""
    if request.method == 'POST':
        # Llamar a la CAPA DE NEGOCIO
        resultado = EventoLogic.eliminar(evento_id, permanente=False)
        
        if resultado['exito']:
            messages.success(request, resultado['mensaje'])
        else:
            messages.error(request, resultado['mensaje'])
    
    return redirect('eventos')
