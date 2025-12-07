"""
CAPA DE PRESENTACIÓN - Views de Lugares
SOLO maneja HTTP - La lógica está en LugarLogic
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ..business.lugar_logic import LugarLogic
from .forms import LugarForm


@login_required
def lista_lugares(request):
    """
    Vista para listar lugares
    SOLO maneja HTTP - sin lógica de negocio
    """
    # Obtener parámetro de búsqueda
    query = request.GET.get('q', '')
    
    # Llamar a la CAPA DE NEGOCIO
    if query:
        lugares = LugarLogic.buscar(query)
    else:
        lugares = LugarLogic.obtener_todos()
    
    # El template espera 'lugares' directamente, no paginación
    context = {
        'lugares': lugares,
        'query': query,
    }
    
    # Usar el template del proyecto original
    return render(request, 'lugares/lista_lugares.html', context)


@login_required
def crear_lugar(request):
    """Vista para crear un lugar"""
    if request.method == 'POST':
        try:
            # El template usa campos HTML directos, no Django forms
            # Llamar a la CAPA DE NEGOCIO directamente con los datos del POST
            resultado = LugarLogic.crear(
                nombre=request.POST.get('nombre', ''),
                descripcion=request.POST.get('descripcion', ''),
                direccion=request.POST.get('direccion', ''),
                latitud=float(request.POST.get('latitud', 0)),
                longitud=float(request.POST.get('longitud', 0)),
                url_mapa=request.POST.get('url_mapa', ''),
                usuario=request.user
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
                return redirect('lista_lugares')
            else:
                messages.error(request, resultado['mensaje'])
        except ValueError as e:
            messages.error(request, f'Error en los datos: {e}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {e}')
    
    # Usar el template del proyecto original
    return render(request, 'lugares/agregar_lugar.html')


@login_required
def editar_lugar(request, lugar_id):
    """Vista para editar un lugar"""
    # Obtener lugar
    resultado = LugarLogic.obtener_por_id(lugar_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
        return redirect('lista_lugares')
    
    lugar = resultado['lugar']
    
    if request.method == 'POST':
        form = LugarForm(request.POST, instance=lugar)
        
        if form.is_valid():
            # Llamar a la CAPA DE NEGOCIO
            resultado = LugarLogic.actualizar(
                lugar_id=lugar_id,
                **form.cleaned_data
            )
            
            if resultado['exito']:
                messages.success(request, resultado['mensaje'])
                return redirect('lista_lugares')
            else:
                messages.error(request, resultado['mensaje'])
    else:
        form = LugarForm(instance=lugar)
    
    # Usar el template del proyecto original
    return render(request, 'lugares/editar_lugar.html', {
        'form': form,
        'lugar': lugar
    })


@login_required
def eliminar_lugar(request, lugar_id):
    """Vista para eliminar un lugar"""
    if request.method == 'POST':
        # Llamar a la CAPA DE NEGOCIO
        resultado = LugarLogic.eliminar(lugar_id, permanente=False)
        
        if resultado['exito']:
            messages.success(request, resultado['mensaje'])
        else:
            messages.error(request, resultado['mensaje'])
        
        return redirect('lista_lugares')
    
    # GET: Mostrar confirmación (redirigir a lista por ahora)
    resultado = LugarLogic.obtener_por_id(lugar_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
    
    return redirect('lista_lugares')


@login_required
def lugares_cercanos(request):
    """Vista para buscar lugares cercanos"""
    # Obtener parámetros
    latitud = float(request.GET.get('lat', -9.3))
    longitud = float(request.GET.get('lon', -75.9))
    radio = int(request.GET.get('radio', 5))
    
    # Llamar a la CAPA DE NEGOCIO
    lugares = LugarLogic.buscar_cercanos(latitud, longitud, radio)
    
    context = {
        'lugares': lugares,
        'latitud': latitud,
        'longitud': longitud,
        'radio': radio
    }
    
    # Mostrar en la misma lista de lugares
    return render(request, 'lugares/lista_lugares.html', context)


@login_required
def detalle_lugar(request, lugar_id):
    """Vista para ver detalle de un lugar"""
    resultado = LugarLogic.obtener_por_id(lugar_id)
    
    if not resultado['exito']:
        messages.error(request, resultado['mensaje'])
    
    return redirect('lista_lugares')
