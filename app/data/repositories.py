"""
CAPA DE DATOS - Repositories
Contiene SOLO operaciones de acceso a datos (CRUD)
Sin lógica de negocio
"""

from django.db import transaction
from django.db.models import Q
from .models import Lugar, Evento, CustomUser


class LugarRepository:
    """
    Repositorio para operaciones de datos de Lugares
    SOLO interactúa con la base de datos
    """
    
    @staticmethod
    def crear(nombre, descripcion, direccion, latitud, longitud, url_mapa=None, creado_por=None):
        """Crear un lugar en la base de datos"""
        with transaction.atomic():
            lugar = Lugar.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                direccion=direccion,
                latitud=latitud,
                longitud=longitud,
                url_mapa=url_mapa,
                creado_por=creado_por
            )
        return lugar
    
    @staticmethod
    def obtener_por_id(lugar_id):
        """Obtener un lugar por ID"""
        try:
            return Lugar.objects.get(id=lugar_id, activo=True)
        except Lugar.DoesNotExist:
            return None
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los lugares (incluidos inactivos)"""
        return Lugar.objects.all()
    
    @staticmethod
    def obtener_activos():
        """Obtener solo lugares activos"""
        return Lugar.objects.filter(activo=True)
    
    @staticmethod
    def buscar(query):
        """Buscar lugares por nombre, descripción o dirección"""
        return Lugar.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(direccion__icontains=query),
            activo=True
        )
    
    @staticmethod
    def actualizar(lugar, **datos):
        """Actualizar un lugar existente"""
        for campo, valor in datos.items():
            if hasattr(lugar, campo):
                setattr(lugar, campo, valor)
        
        lugar.save()
        return lugar
    
    @staticmethod
    def eliminar_logico(lugar):
        """Soft delete - marcar como inactivo"""
        lugar.activo = False
        lugar.save()
        return True
    
    @staticmethod
    def eliminar_permanente(lugar):
        """Hard delete - eliminar de la base de datos"""
        lugar.delete()
        return True
    
    @staticmethod
    def contar_activos():
        """Contar lugares activos"""
        return Lugar.objects.filter(activo=True).count()
    
    @staticmethod
    def contar_por_usuario(usuario):
        """Contar lugares creados por un usuario"""
        return Lugar.objects.filter(creado_por=usuario, activo=True).count()


class EventoRepository:
    """
    Repositorio para operaciones de datos de Eventos
    """
    
    @staticmethod
    def crear(titulo, descripcion, fecha_inicio, fecha_fin, lugar, capacidad_maxima, creado_por=None):
        """Crear un evento en la base de datos"""
        with transaction.atomic():
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                lugar=lugar,
                capacidad_maxima=capacidad_maxima,
                creado_por=creado_por
            )
        return evento
    
    @staticmethod
    def obtener_por_id(evento_id):
        """Obtener un evento por ID"""
        try:
            return Evento.objects.get(id=evento_id, activo=True)
        except Evento.DoesNotExist:
            return None
    
    @staticmethod
    def obtener_activos():
        """Obtener eventos activos"""
        return Evento.objects.filter(activo=True)
    
    @staticmethod
    def obtener_proximos():
        """Obtener eventos futuros"""
        from django.utils import timezone
        return Evento.objects.filter(
            activo=True,
            fecha_inicio__gte=timezone.now()
        ).order_by('fecha_inicio')
    
    @staticmethod
    def buscar(query):
        """Buscar eventos por título o descripción"""
        from django.db.models import Q
        return Evento.objects.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query),
            activo=True
        )
    
    @staticmethod
    def inscribir_usuario(evento, usuario):
        """Inscribir un usuario en un evento"""
        evento.inscritos.add(usuario)
        return evento
    
    @staticmethod
    def desinscribir_usuario(evento, usuario):
        """Desinscribir un usuario de un evento"""
        evento.inscritos.remove(usuario)
        return evento
    
    @staticmethod
    def actualizar(evento, **datos):
        """Actualizar un evento"""
        for campo, valor in datos.items():
            if hasattr(evento, campo):
                setattr(evento, campo, valor)
        
        evento.save()
        return evento
    
    @staticmethod
    def eliminar_logico(evento):
        """Soft delete de evento"""
        evento.activo = False
        evento.save()
        return True
    
    @staticmethod
    def eliminar_permanente(evento):
        """Hard delete de evento"""
        evento.delete()
        return True


class UserRepository:
    """
    Repositorio para operaciones con usuarios
    """
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los usuarios"""
        return CustomUser.objects.all()
    
    @staticmethod
    def obtener_por_id(user_id):
        """Obtener usuario por ID"""
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def obtener_por_username(username):
        """Obtener usuario por username"""
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def crear(username, email, password, **extra_fields):
        """Crear un nuevo usuario"""
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        return user
    
    @staticmethod
    def actualizar(user_id, **datos):
        """Actualizar un usuario"""
        try:
            user = CustomUser.objects.get(id=user_id)
            
            for campo, valor in datos.items():
                if hasattr(user, campo):
                    setattr(user, campo, valor)
            
            user.save()
            return user
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def eliminar(user_id):
        """Eliminar un usuario"""
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False
