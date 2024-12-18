from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Permite acceso total a los administradores y solo lectura a los usuarios regulares.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True  # Permitir lectura a todos
        return request.user.is_staff  # Permitir escritura solo a superusuarios

class IsSelfOrReadOnly(BasePermission):
    """
    Permite a los usuarios ver y editar solo su propia información.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True  # Permitir lectura a todos
        return obj == request.user  # Solo puede editar su propio perfil
