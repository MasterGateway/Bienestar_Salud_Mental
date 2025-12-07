"""
URLs de la Aplicación - ARQUITECTURA EN CAPAS
Rutas organizadas por módulo
"""

from django.urls import path
from .presentation import auth_views, lugar_views, evento_views, user_views

urlpatterns = [
    # ========== AUTENTICACIÓN ==========
    path('', auth_views.home_view, name='home'),
    path('inicio/', auth_views.nueva_pagina_view, name='inicio'),  # Alias para inicio
    path('nueva_pagina/', auth_views.nueva_pagina_view, name='nueva_pagina'),  # Página de inicio
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('contact/', auth_views.contact_view, name='contacto'),  # Vista de contacto
    
    # ========== LUGARES ==========
    path('lugares/', lugar_views.lista_lugares, name='lista_lugares'),
    path('lugares/crear/', lugar_views.crear_lugar, name='crear_lugar'),
    path('lugares/agregar/', lugar_views.crear_lugar, name='agregar_lugar_usuario'),  # Alias para compatibilidad
    path('lugares/<int:lugar_id>/', lugar_views.detalle_lugar, name='detalle_lugar'),
    path('lugares/<int:lugar_id>/editar/', lugar_views.editar_lugar, name='editar_lugar'),
    path('lugares/<int:lugar_id>/eliminar/', lugar_views.eliminar_lugar, name='eliminar_lugar'),
    path('lugares/cercanos/', lugar_views.lugares_cercanos, name='lugares_cercanos'),
    
    # ========== EVENTOS ==========
    path('eventos/', evento_views.lista_eventos, name='eventos'),  # Nombre compatible
    path('eventos/lista/', evento_views.lista_eventos, name='lista_eventos'),
    path('eventos/crear/', evento_views.crear_evento, name='crear_evento'),
    path('eventos/<int:evento_id>/', evento_views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:evento_id>/editar/', evento_views.editar_evento, name='editar_evento'),
    path('eventos/<int:evento_id>/eliminar/', evento_views.eliminar_evento, name='eliminar_evento'),
    path('eventos/<int:evento_id>/inscribir/', evento_views.inscribir_evento, name='inscribir_evento'),
    path('eventos/<int:evento_id>/desinscribir/', evento_views.desinscribir_evento, name='desinscribir_evento'),
    path('eventos/mis-eventos/', evento_views.mis_eventos, name='mis_eventos'),
    
    # ========== USUARIOS ==========
    path('usuarios/', user_views.lista_usuarios, name='lista_usuarios'),
    path('perfil/', user_views.perfil_usuario, name='perfil_usuario'),
    path('usuarios/<int:user_id>/', user_views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:user_id>/editar/', user_views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/eliminar/', user_views.eliminar_usuario, name='eliminar_usuario'),
]
