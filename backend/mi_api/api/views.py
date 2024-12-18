from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Evento, Participante
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    CategoriaSerializer,
    EventoSerializer,
    ParticipanteSerializer
)
from django.contrib.auth.models import User
from .permissions import IsAdminOrReadOnly, IsSelfOrReadOnly

# Token personalizado
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Registro de usuario
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = True  # Asegurar que el usuario esté activo
        user.save()
        return Response({"message": "Usuario registrado con éxito."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Listar usuarios
@api_view(['GET'])
def listar_usuarios(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Autenticación requerida."}, status=status.HTTP_401_UNAUTHORIZED)

    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)

# Vista para Categorías
class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo administradores pueden escribir

# Vista para Eventos
class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo administradores pueden escribir
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria', 'fecha']  # Filtros disponibles

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria')
        fecha = self.request.query_params.get('fecha')
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        return queryset

# Vista para Participantes
class ParticipanteViewSet(ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get_queryset(self):
        """
        Los usuarios regulares solo pueden ver sus propias inscripciones.
        """
        if self.request.user.is_staff:
            return super().get_queryset()  # Admins ven todo
        return Participante.objects.filter(correo=self.request.user.email)

    def perform_create(self, serializer):
        """
        Asigna automáticamente el correo del usuario autenticado al registro.
        """
        serializer.save(correo=self.request.user.email)

# Endpoint para obtener eventos inscritos por el usuario actual
@api_view(['GET'])
def eventos_inscritos(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Autenticación requerida."}, status=status.HTTP_401_UNAUTHORIZED)

    inscritos = Participante.objects.filter(correo=request.user.email)
    serializer = ParticipanteSerializer(inscritos, many=True)
    return Response(serializer.data)
