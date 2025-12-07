# ARQUITECTURA EN CAPAS - Proyecto Django

## 📋 Descripción
Este proyecto implementa **ARQUITECTURA EN CAPAS (Layered Architecture)** con 3 capas bien definidas:

```
PRESENTACIÓN (HTTP)
       ↓
    NEGOCIO (Lógica)
       ↓
    DATOS (Base de Datos)
```

## 📁 Estructura del Proyecto

```
proyecto_capas/
│
├── config/                      # Configuración de Django
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py / asgi.py       # Servidores
│   └── __init__.py
│
├── app/                         # Aplicación principal
│   │
│   ├── data/                    # 🗄️ CAPA DE DATOS
│   │   ├── models.py           # Modelos Django (CustomUser, Lugar, Evento)
│   │   ├── repositories.py     # Acceso a base de datos (CRUD)
│   │   └── __init__.py
│   │
│   ├── business/                # 💼 CAPA DE NEGOCIO
│   │   ├── lugar_logic.py      # Lógica de lugares
│   │   ├── evento_logic.py     # Lógica de eventos
│   │   ├── user_logic.py       # Lógica de usuarios
│   │   └── __init__.py
│   │
│   ├── presentation/            # 🌐 CAPA DE PRESENTACIÓN
│   │   ├── forms.py            # Formularios Django
│   │   ├── auth_views.py       # Vistas de autenticación
│   │   ├── lugar_views.py      # Vistas de lugares
│   │   ├── evento_views.py     # Vistas de eventos
│   │   ├── user_views.py       # Vistas de usuarios
│   │   └── __init__.py
│   │
│   ├── admin.py                # Configuración del admin
│   ├── urls.py                 # URLs de la app
│   └── __init__.py
│
├── templates/                   # Plantillas HTML (pendiente)
├── static/                      # Archivos estáticos (pendiente)
├── manage.py                    # CLI de Django
└── README.md                    # Este archivo
```

## 🎯 Responsabilidades de Cada Capa

### 1️⃣ CAPA DE DATOS (`app/data/`)
**SOLO** acceso a la base de datos. SIN lógica de negocio.

#### `models.py`
- Define la estructura de la base de datos
- Modelos: `CustomUser`, `Lugar`, `Evento`
- Properties útiles: `esta_lleno`, `plazas_disponibles`

#### `repositories.py`
- CRUD puro (Create, Read, Update, Delete)
- Clases: `UserRepository`, `LugarRepository`, `EventoRepository`
- Métodos: `crear()`, `obtener_por_id()`, `actualizar()`, `eliminar()`

### 2️⃣ CAPA DE NEGOCIO (`app/business/`)
**TODA** la lógica de la aplicación. AQUÍ van las validaciones y reglas.

#### `lugar_logic.py`
- Validaciones: nombre mínimo 3 caracteres, coordenadas válidas, etc.
- Lógica geoespacial: cálculo de distancia con fórmula de Haversine
- Métodos: `crear()`, `buscar_cercanos()`, `actualizar()`, `eliminar()`

#### `evento_logic.py`
- Validaciones: capacidad, fechas, disponibilidad
- Lógica de inscripciones: verificar cupos, duplicados, etc.
- Métodos: `crear()`, `inscribir_usuario()`, `desinscribir_usuario()`

#### `user_logic.py`
- Validaciones: contraseñas, emails, usernames únicos
- Autenticación y registro
- Métodos: `registrar()`, `autenticar()`, `actualizar()`

### 3️⃣ CAPA DE PRESENTACIÓN (`app/presentation/`)
**SOLO** maneja HTTP (requests/responses). SIN lógica de negocio.

#### `forms.py`
- Formularios Django para validación de entrada
- Forms: `CustomUserCreationForm`, `LugarForm`, `EventoForm`

#### `auth_views.py`, `lugar_views.py`, `evento_views.py`, `user_views.py`
- Manejan requests HTTP
- Llaman a la capa de negocio
- Retornan templates o redirects
- Usan Django messages para feedback

## 🔄 Flujo de Datos

```
Usuario hace request
       ↓
Vista (Presentation) recibe request
       ↓
Vista llama a Lógica (Business)
       ↓
Lógica valida y llama a Repository (Data)
       ↓
Repository consulta Base de Datos
       ↓
Datos suben por las capas
       ↓
Vista retorna response al usuario
```

### Ejemplo Concreto: Crear un Lugar

```python
# 1. Usuario envía formulario → lugar_views.py (PRESENTACIÓN)
def crear_lugar(request):
    if request.method == 'POST':
        form = LugarForm(request.POST)
        
        if form.is_valid():
            # 2. Vista llama a NEGOCIO
            resultado = LugarLogic.crear(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                ...
            )

# 3. LugarLogic valida (NEGOCIO)
class LugarLogic:
    @staticmethod
    def crear(...):
        # Validaciones
        if len(nombre) < 3:
            return {'exito': False, 'mensaje': 'Nombre muy corto'}
        
        # 4. Llama a DATOS
        lugar = LugarRepository.crear(...)
        return {'exito': True, 'lugar': lugar}

# 5. Repository guarda en BD (DATOS)
class LugarRepository:
    @staticmethod
    def crear(...):
        lugar = Lugar.objects.create(...)
        return lugar
```

## ✅ Ventajas de Esta Arquitectura

1. **Separación Clara**: Cada capa tiene una responsabilidad única
2. **Fácil de Testear**: Puedes probar cada capa independientemente
3. **Mantenible**: Cambios en una capa no afectan a otras
4. **Reutilizable**: La lógica de negocio puede usarse desde API, CLI, etc.
5. **Escalable**: Fácil agregar nuevas funcionalidades

## 🚀 Cómo Usarlo

### Instalación
```bash
cd proyecto_capas
pip install django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### URLs Disponibles
- `/` - Home
- `/login/` - Login
- `/register/` - Registro
- `/lugares/` - Lista de lugares
- `/eventos/` - Lista de eventos
- `/admin/` - Panel de administración

## 📊 Comparación con tu Proyecto Actual

### Proyecto Actual (MVT Monolítico)
```python
# views.py - TODO mezclado
def crear_lugar(request):
    if request.method == 'POST':
        # Validación mezclada con lógica
        if len(nombre) < 3:
            messages.error(...)
        # Guardado directo
        Lugar.objects.create(...)
```

### Con Arquitectura en Capas
```python
# presentation/lugar_views.py - SOLO HTTP
def crear_lugar(request):
    resultado = LugarLogic.crear(...)  # Delega a negocio
    
# business/lugar_logic.py - SOLO lógica
def crear():
    # Validaciones aquí
    LugarRepository.crear(...)  # Delega a datos
    
# data/repositories.py - SOLO base de datos
def crear():
    Lugar.objects.create(...)
```

## 🎓 Conceptos Clave

1. **Unidireccional**: El flujo SIEMPRE va de arriba hacia abajo
   - ✅ Presentación → Negocio → Datos
   - ❌ NUNCA: Datos → Negocio → Presentación

2. **Acoplamiento Bajo**: Cada capa solo conoce a la capa inferior
   - Presentación conoce a Negocio
   - Negocio conoce a Datos
   - Datos NO conoce a nadie

3. **Alta Cohesión**: Cada capa agrupa código relacionado
   - Todo lo de HTTP en Presentación
   - Toda la lógica en Negocio
   - Todo el acceso a BD en Datos

## 📝 Notas Importantes

- **PENDIENTE**: Templates HTML (se usarían plantillas básicas)
- **PENDIENTE**: Archivos estáticos (CSS, JS)
- Este es un ejemplo funcional pero necesita templates para funcionar completamente
- Puedes usar el Django Admin (`/admin/`) para probar la funcionalidad

## 🔍 ¿Qué Módulos Hay?

### Módulos de Negocio:
1. **Gestión de Usuarios**: Registro, login, perfiles
2. **Gestión de Lugares**: CRUD + búsqueda geoespacial
3. **Gestión de Eventos**: CRUD + inscripciones con control de cupos

### Cada módulo tiene 3 archivos:
- `data/repositories.py` → Acceso a BD
- `business/*_logic.py` → Lógica y validaciones
- `presentation/*_views.py` → Manejo HTTP
