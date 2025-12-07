"""
Configuración del Admin - ARQUITECTURA EN CAPAS
"""

from django.contrib import admin
from .data.models import CustomUser, Lugar, Evento


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin para usuarios personalizados"""
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'bio')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('username', 'email', 'password')
        }),
        ('Información Personal', {
            'fields': ('bio', 'telefono')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    """Admin para lugares"""
    list_display = ('nombre', 'direccion', 'activo', 'creado_por', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'direccion')
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'direccion')
        }),
        ('Ubicación', {
            'fields': ('latitud', 'longitud', 'url_mapa'),
            'description': 'Coordenadas geográficas del lugar'
        }),
        ('Metadata', {
            'fields': ('activo', 'creado_por', 'fecha_creacion')
        }),
    )
    
    readonly_fields = ('fecha_creacion',)
    
    def save_model(self, request, obj, form, change):
        """Asignar usuario creador si es nuevo"""
        if not change:  # Si es un objeto nuevo
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Admin para eventos"""
    list_display = ('titulo', 'lugar', 'fecha_inicio', 'capacidad_maxima', 'plazas_disponibles', 'esta_lleno', 'activo')
    list_filter = ('activo', 'fecha_inicio', 'lugar')
    search_fields = ('titulo', 'descripcion', 'lugar__nombre')
    ordering = ('-fecha_inicio',)
    filter_horizontal = ('inscritos',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'lugar')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Capacidad', {
            'fields': ('capacidad_maxima', 'inscritos'),
            'description': 'Gestión de capacidad y participantes'
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ('plazas_disponibles', 'esta_lleno')
    
    def get_readonly_fields(self, request, obj=None):
        """Campos de solo lectura dinámicos"""
        readonly = list(self.readonly_fields)
        if obj:  # Si está editando
            readonly.extend(['plazas_disponibles', 'esta_lleno'])
        return readonly
