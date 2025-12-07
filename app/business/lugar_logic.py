"""
CAPA DE NEGOCIO - Lógica de Lugares
Contiene TODA la lógica de negocio y validaciones
"""

import math
from ..data.repositories import LugarRepository


class LugarLogic:
    """
    Lógica de negocio para Lugares
    Sin dependencias de Django/HTTP
    """
    
    @staticmethod
    def crear(nombre, descripcion, direccion, latitud, longitud, url_mapa=None, usuario=None):
        """
        Crear un lugar con todas las validaciones de negocio
        
        Args:
            nombre (str): Nombre del lugar
            descripcion (str): Descripción
            direccion (str): Dirección física
            latitud (float): Coordenada latitud
            longitud (float): Coordenada longitud
            url_mapa (str, optional): URL del mapa
            usuario (User, optional): Usuario que crea
            
        Returns:
            dict: {'exito': bool, 'mensaje': str, 'lugar': Lugar}
        """
        # VALIDACIÓN 1: Nombre mínimo 3 caracteres
        if not nombre or len(nombre.strip()) < 3:
            return {
                'exito': False,
                'mensaje': 'El nombre debe tener al menos 3 caracteres',
                'lugar': None
            }
        
        # VALIDACIÓN 2: Descripción no vacía
        if not descripcion or len(descripcion.strip()) < 10:
            return {
                'exito': False,
                'mensaje': 'La descripción debe tener al menos 10 caracteres',
                'lugar': None
            }
        
        # VALIDACIÓN 3: Dirección no vacía
        if not direccion or len(direccion.strip()) < 5:
            return {
                'exito': False,
                'mensaje': 'La dirección debe tener al menos 5 caracteres',
                'lugar': None
            }
        
        # VALIDACIÓN 4: Latitud válida
        if not (-90 <= latitud <= 90):
            return {
                'exito': False,
                'mensaje': f'Latitud inválida ({latitud}). Debe estar entre -90 y 90',
                'lugar': None
            }
        
        # VALIDACIÓN 5: Longitud válida
        if not (-180 <= longitud <= 180):
            return {
                'exito': False,
                'mensaje': f'Longitud inválida ({longitud}). Debe estar entre -180 y 180',
                'lugar': None
            }
        
        # LÓGICA DE NEGOCIO: Generar URL de mapa si no se proporciona
        if not url_mapa:
            url_mapa = f"https://www.google.com/maps?q={latitud},{longitud}"
        
        # CREAR usando la capa de datos
        lugar = LugarRepository.crear(
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            direccion=direccion.strip(),
            latitud=latitud,
            longitud=longitud,
            url_mapa=url_mapa,
            creado_por=usuario
        )
        
        return {
            'exito': True,
            'mensaje': f'Lugar "{nombre}" creado exitosamente',
            'lugar': lugar
        }
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los lugares activos"""
        return LugarRepository.obtener_activos()
    
    @staticmethod
    def obtener_por_id(lugar_id):
        """Obtener un lugar por ID"""
        lugar = LugarRepository.obtener_por_id(lugar_id)
        
        if not lugar:
            return {
                'exito': False,
                'mensaje': 'Lugar no encontrado',
                'lugar': None
            }
        
        return {
            'exito': True,
            'mensaje': 'Lugar encontrado',
            'lugar': lugar
        }
    
    @staticmethod
    def buscar(query):
        """
        Buscar lugares por texto
        
        Args:
            query (str): Término de búsqueda
            
        Returns:
            QuerySet: Lugares que coinciden
        """
        if not query or len(query.strip()) < 2:
            return LugarRepository.obtener_activos()
        
        return LugarRepository.buscar(query.strip())
    
    @staticmethod
    def buscar_cercanos(latitud, longitud, radio_km=5):
        """
        LÓGICA DE NEGOCIO: Buscar lugares dentro de un radio
        
        Args:
            latitud (float): Latitud central
            longitud (float): Longitud central
            radio_km (float): Radio en kilómetros
            
        Returns:
            list: Lista de diccionarios con lugar y distancia
        """
        # VALIDAR coordenadas
        if not (-90 <= latitud <= 90):
            return []
        
        if not (-180 <= longitud <= 180):
            return []
        
        # Obtener todos los lugares
        todos_lugares = LugarRepository.obtener_activos()
        
        lugares_cercanos = []
        
        for lugar in todos_lugares:
            # LÓGICA DE NEGOCIO: Calcular distancia
            distancia = LugarLogic._calcular_distancia(
                latitud, longitud,
                lugar.latitud, lugar.longitud
            )
            
            if distancia <= radio_km:
                lugares_cercanos.append({
                    'lugar': lugar,
                    'distancia_km': round(distancia, 2)
                })
        
        # Ordenar por distancia (más cercanos primero)
        lugares_cercanos.sort(key=lambda x: x['distancia_km'])
        
        return lugares_cercanos
    
    @staticmethod
    def actualizar(lugar_id, **datos):
        """
        Actualizar un lugar con validaciones
        
        Args:
            lugar_id (int): ID del lugar
            **datos: Datos a actualizar
            
        Returns:
            dict: Resultado de la operación
        """
        # VALIDACIÓN: Lugar existe
        lugar = LugarRepository.obtener_por_id(lugar_id)
        if not lugar:
            return {
                'exito': False,
                'mensaje': 'Lugar no encontrado',
                'lugar': None
            }
        
        # VALIDACIÓN: Nombre si se proporciona
        if 'nombre' in datos and len(datos['nombre'].strip()) < 3:
            return {
                'exito': False,
                'mensaje': 'El nombre debe tener al menos 3 caracteres',
                'lugar': None
            }
        
        # VALIDACIÓN: Latitud si se proporciona
        if 'latitud' in datos and not (-90 <= datos['latitud'] <= 90):
            return {
                'exito': False,
                'mensaje': 'Latitud inválida',
                'lugar': None
            }
        
        # VALIDACIÓN: Longitud si se proporciona
        if 'longitud' in datos and not (-180 <= datos['longitud'] <= 180):
            return {
                'exito': False,
                'mensaje': 'Longitud inválida',
                'lugar': None
            }
        
        # ACTUALIZAR
        lugar_actualizado = LugarRepository.actualizar(lugar, **datos)
        
        return {
            'exito': True,
            'mensaje': 'Lugar actualizado correctamente',
            'lugar': lugar_actualizado
        }
    
    @staticmethod
    def eliminar(lugar_id, permanente=False):
        """
        Eliminar un lugar (soft delete por defecto)
        
        Args:
            lugar_id (int): ID del lugar
            permanente (bool): Si True, elimina de DB
            
        Returns:
            dict: Resultado de la operación
        """
        # VALIDACIÓN: Lugar existe
        lugar = LugarRepository.obtener_por_id(lugar_id)
        if not lugar:
            return {
                'exito': False,
                'mensaje': 'Lugar no encontrado'
            }
        
        # LÓGICA DE NEGOCIO: Soft delete por defecto
        if permanente:
            exito = LugarRepository.eliminar_permanente(lugar)
            mensaje = 'Lugar eliminado permanentemente'
        else:
            exito = LugarRepository.eliminar_logico(lugar)
            mensaje = 'Lugar desactivado correctamente'
        
        return {
            'exito': exito,
            'mensaje': mensaje
        }
    
    @staticmethod
    def obtener_estadisticas():
        """
        LÓGICA DE NEGOCIO: Obtener estadísticas de lugares
        
        Returns:
            dict: Estadísticas
        """
        total = LugarRepository.contar_activos()
        
        return {
            'total_lugares': total,
            'lugares_recientes': total  # Puedes expandir esto
        }
    
    @staticmethod
    def _calcular_distancia(lat1, lon1, lat2, lon2):
        """
        LÓGICA PRIVADA: Calcular distancia entre dos puntos usando Haversine
        
        Args:
            lat1, lon1: Coordenadas del punto 1
            lat2, lon2: Coordenadas del punto 2
            
        Returns:
            float: Distancia en kilómetros
        """
        R = 6371  # Radio de la Tierra en kilómetros
        
        # Convertir grados a radianes
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Fórmula de Haversine
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distancia = R * c
        
        return distancia
