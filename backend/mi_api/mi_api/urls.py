"""
URL configuration for mi_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from api.views import (
    CategoriaViewSet,
    EventoViewSet,
    ParticipanteViewSet,
    register_user,
    CustomTokenObtainPairView,
    eventos_inscritos,
    listar_usuarios,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# Configurar router para las rutas de la API
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'eventos', EventoViewSet, basename='eventos')
router.register(r'participantes', ParticipanteViewSet, basename='participantes')

urlpatterns = [
    # Rutas de administración
    path('admin/', admin.site.urls),

    # Rutas base para la API
    path('api/', include(router.urls)),

    # Ruta para registrar usuarios
    path('api/register/', register_user, name='register_user'),

    # Rutas para autenticación con JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas adicionales
    path('api/eventos-inscritos/', eventos_inscritos, name='eventos_inscritos'),
    path('api/usuarios/', listar_usuarios, name='listar_usuarios'),  # Ruta para listar usuarios registrados

    path('docs/', include_docs_urls(title='API Documentation', permission_classes=[])), 
]
