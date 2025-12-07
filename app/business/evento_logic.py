"""
CAPA DE NEGOCIO - Lógica de Eventos
"""

from datetime import datetime
from django.utils import timezone
from ..data.repositories import EventoRepository, LugarRepository


class EventoLogic:
    """
    Lógica de negocio para Eventos
    """
    
    @staticmethod
    def crear(titulo, descripcion, fecha_inicio, fecha_fin, lugar_id, capacidad_maxima, usuario=None):
        """
        Crear un evento con validaciones de negocio
        
        Returns:
            dict: {'exito': bool, 'mensaje': str, 'evento': Evento}
        """
        # VALIDACIÓN 1: Título mínimo
        if not titulo or len(titulo.strip()) < 5:
            return {
                'exito': False,
                'mensaje': 'El título debe tener al menos 5 caracteres',
                'evento': None
            }
        
        # VALIDACIÓN 2: Descripción
        if not descripcion or len(descripcion.strip()) < 20:
            return {
                'exito': False,
                'mensaje': 'La descripción debe tener al menos 20 caracteres',
                'evento': None
            }
        
        # VALIDACIÓN 3: Fecha inicio en el futuro
        if fecha_inicio < timezone.now():
            return {
                'exito': False,
                'mensaje': 'La fecha de inicio debe ser en el futuro',
                'evento': None
            }
        
        # VALIDACIÓN 4: Fecha fin después de inicio
        if fecha_fin <= fecha_inicio:
            return {
                'exito': False,
                'mensaje': 'La fecha de fin debe ser posterior a la de inicio',
                'evento': None
            }
        
        # VALIDACIÓN 5: Capacidad mínima
        if capacidad_maxima < 1:
            return {
                'exito': False,
                'mensaje': 'La capacidad debe ser al menos 1 persona',
                'evento': None
            }
        
        # VALIDACIÓN 6: Lugar existe
        lugar = LugarRepository.obtener_por_id(lugar_id)
        if not lugar:
            return {
                'exito': False,
                'mensaje': 'El lugar especificado no existe',
                'evento': None
            }
        
        # CREAR evento
        evento = EventoRepository.crear(
            titulo=titulo.strip(),
            descripcion=descripcion.strip(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            lugar=lugar,
            capacidad_maxima=capacidad_maxima,
            creado_por=usuario
        )
        
        return {
            'exito': True,
            'mensaje': f'Evento "{titulo}" creado exitosamente',
            'evento': evento
        }
    
    @staticmethod
    def obtener_proximos():
        """Obtener eventos próximos"""
        return EventoRepository.obtener_proximos()
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los eventos activos"""
        return EventoRepository.obtener_activos()
    
    @staticmethod
    def obtener_disponibles():
        """Obtener eventos con plazas disponibles"""
        eventos = EventoRepository.obtener_activos()
        return [e for e in eventos if not e.esta_lleno]
    
    @staticmethod
    def obtener_por_id(evento_id):
        """Obtener evento por ID"""
        evento = EventoRepository.obtener_por_id(evento_id)
        if evento:
            return {
                'exito': True,
                'mensaje': 'Evento encontrado',
                'evento': evento
            }
        return {
            'exito': False,
            'mensaje': 'Evento no encontrado',
            'evento': None
        }
    
    @staticmethod
    def obtener_por_usuario(user_id):
        """Obtener eventos donde el usuario está inscrito"""
        from ..data.models import Evento
        return Evento.objects.filter(inscritos__id=user_id, activo=True)
    
    @staticmethod
    def buscar(query):
        """Buscar eventos por título o descripción"""
        return EventoRepository.buscar(query)
    
    @staticmethod
    def actualizar(evento_id, **kwargs):
        """Actualizar un evento"""
        evento = EventoRepository.obtener_por_id(evento_id)
        if not evento:
            return {
                'exito': False,
                'mensaje': 'Evento no encontrado'
            }
        
        EventoRepository.actualizar(evento, **kwargs)
        return {
            'exito': True,
            'mensaje': 'Evento actualizado correctamente',
            'evento': evento
        }
    
    @staticmethod
    def eliminar(evento_id, permanente=False):
        """Eliminar un evento"""
        evento = EventoRepository.obtener_por_id(evento_id)
        if not evento:
            return {
                'exito': False,
                'mensaje': 'Evento no encontrado'
            }
        
        if permanente:
            EventoRepository.eliminar_permanente(evento)
            mensaje = 'Evento eliminado permanentemente'
        else:
            EventoRepository.eliminar_logico(evento)
            mensaje = 'Evento desactivado correctamente'
        
        return {
            'exito': True,
            'mensaje': mensaje
        }
    
    @staticmethod
    def inscribir_usuario(evento_id, user_id):
        """
        Inscribir un usuario en un evento con validaciones
        
        Returns:
            dict: Resultado de la operación
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Obtener usuario
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {
                'exito': False,
                'mensaje': 'Usuario no encontrado'
            }
        # Obtener usuario
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {
                'exito': False,
                'mensaje': 'Usuario no encontrado'
            }
        
        # VALIDACIÓN 1: Evento existe
        evento = EventoRepository.obtener_por_id(evento_id)
        if not evento:
            return {
                'exito': False,
                'mensaje': 'Evento no encontrado'
            }
        
        # VALIDACIÓN 2: Evento no está lleno
        if evento.esta_lleno:
            return {
                'exito': False,
                'mensaje': f'El evento está lleno (capacidad: {evento.capacidad_maxima})'
            }
        
        # VALIDACIÓN 3: Usuario no inscrito previamente
        if evento.inscritos.filter(id=usuario.id).exists():
            return {
                'exito': False,
                'mensaje': 'Ya estás inscrito en este evento'
            }
        
        # VALIDACIÓN 4: Evento no ha pasado
        if evento.fecha_inicio < timezone.now():
            return {
                'exito': False,
                'mensaje': 'Este evento ya ha comenzado'
            }
        
        # INSCRIBIR
        EventoRepository.inscribir_usuario(evento, usuario)
        
        return {
            'exito': True,
            'mensaje': f'Te has inscrito en "{evento.titulo}" correctamente'
        }
    
    @staticmethod
    def desinscribir_usuario(evento_id, user_id):
        """Desinscribir usuario de un evento"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Obtener usuario
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {
                'exito': False,
                'mensaje': 'Usuario no encontrado'
            }
        
        evento = EventoRepository.obtener_por_id(evento_id)
        
        if not evento:
            return {
                'exito': False,
                'mensaje': 'Evento no encontrado'
            }
        
        if not evento.inscritos.filter(id=usuario.id).exists():
            return {
                'exito': False,
                'mensaje': 'No estás inscrito en este evento'
            }
        
        EventoRepository.desinscribir_usuario(evento, usuario)
        
        return {
            'exito': True,
            'mensaje': 'Te has desinscrito correctamente'
        }
