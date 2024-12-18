from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CategoriaViewSet, EventoViewSet, ParticipanteViewSet,
    register_user, CustomTokenObtainPairView, eventos_inscritos
)
from rest_framework_simplejwt.views import TokenRefreshView

# Configurar router para los ViewSets
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'participantes', ParticipanteViewSet)

# Rutas específicas de la aplicación
urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('eventos-inscritos/', eventos_inscritos, name='eventos_inscritos'),
]

urlpatterns += router.urls
