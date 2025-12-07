"""
CAPA DE NEGOCIO - Lógica de Usuarios
"""

from django.contrib.auth import authenticate
from ..data.repositories import UserRepository


class UserLogic:
    """
    Lógica de negocio para Usuarios
    """
    
    @staticmethod
    def registrar(username, email, password, password_confirm):
        """
        Registrar un nuevo usuario con validaciones
        
        Returns:
            dict: {'exito': bool, 'mensaje': str, 'user': User}
        """
        # VALIDACIÓN 1: Username mínimo
        if not username or len(username.strip()) < 3:
            return {
                'exito': False,
                'mensaje': 'El nombre de usuario debe tener al menos 3 caracteres',
                'user': None
            }
        
        # VALIDACIÓN 2: Email válido
        if not email or '@' not in email:
            return {
                'exito': False,
                'mensaje': 'Email inválido',
                'user': None
            }
        
        # VALIDACIÓN 3: Contraseñas coinciden
        if password != password_confirm:
            return {
                'exito': False,
                'mensaje': 'Las contraseñas no coinciden',
                'user': None
            }
        
        # VALIDACIÓN 4: Contraseña mínima
        if len(password) < 6:
            return {
                'exito': False,
                'mensaje': 'La contraseña debe tener al menos 6 caracteres',
                'user': None
            }
        
        # VALIDACIÓN 5: Usuario no existe
        if UserRepository.obtener_por_username(username):
            return {
                'exito': False,
                'mensaje': 'El nombre de usuario ya está en uso',
                'user': None
            }
        
        # CREAR usuario
        try:
            user = UserRepository.crear(
                username=username.strip(),
                email=email.strip(),
                password=password
            )
            
            return {
                'exito': True,
                'mensaje': f'Usuario {username} registrado exitosamente',
                'user': user
            }
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error al registrar usuario: {str(e)}',
                'user': None
            }
    
    @staticmethod
    def autenticar(username, password):
        """
        Autenticar un usuario
        
        Returns:
            dict: {'exito': bool, 'mensaje': str, 'user': User}
        """
        user = authenticate(username=username, password=password)
        
        if user is not None:
            return {
                'exito': True,
                'mensaje': 'Autenticación exitosa',
                'user': user
            }
        else:
            return {
                'exito': False,
                'mensaje': 'Credenciales incorrectas',
                'user': None
            }
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los usuarios"""
        return UserRepository.obtener_todos()
    
    @staticmethod
    def actualizar(user_id, **datos):
        """Actualizar usuario"""
        user = UserRepository.obtener_por_id(user_id)
        
        if not user:
            return {
                'exito': False,
                'mensaje': 'Usuario no encontrado'
            }
        
        user_actualizado = UserRepository.actualizar(user_id, **datos)
        
        return {
            'exito': True,
            'mensaje': 'Usuario actualizado correctamente',
            'user': user_actualizado
        }
    
    @staticmethod
    def eliminar(user_id):
        """Eliminar usuario"""
        user = UserRepository.obtener_por_id(user_id)
        
        if not user:
            return {
                'exito': False,
                'mensaje': 'Usuario no encontrado'
            }
        
        exito = UserRepository.eliminar(user_id)
        
        return {
            'exito': exito,
            'mensaje': 'Usuario eliminado correctamente' if exito else 'Error al eliminar'
        }
