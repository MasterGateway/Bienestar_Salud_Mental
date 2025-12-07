"""
CAPA DE DATOS - Models
Contiene SOLO la estructura de datos, sin lógica de negocio
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """Usuario personalizado - puede extenderse con campos adicionales"""
    bio = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username


class Lugar(models.Model):
    """Modelo de datos para Lugares de bienestar mental"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    url_mapa = models.URLField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)  # Para soft delete
    creado_por = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='lugares_creados'
    )
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
    
    def __str__(self):
        return self.nombre
    
    @property
    def coordenadas(self):
        """Helper para obtener coordenadas formateadas"""
        return f"{self.latitud},{self.longitud}"


class Evento(models.Model):
    """Modelo de datos para Eventos de bienestar"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='eventos')
    capacidad_maxima = models.IntegerField()
    inscritos = models.ManyToManyField(CustomUser, related_name='eventos_inscritos', blank=True)
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='eventos_creados'
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
    
    def __str__(self):
        return self.titulo
    
    @property
    def esta_lleno(self):
        """Helper para verificar si el evento está lleno"""
        return self.inscritos.count() >= self.capacidad_maxima
    
    @property
    def plazas_disponibles(self):
        """Helper para obtener plazas disponibles"""
        return self.capacidad_maxima - self.inscritos.count()
