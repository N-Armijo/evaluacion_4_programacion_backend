from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import BasePermission, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Categoria, Evento, Participante
from .serializers import (
    CategoriaSerializer,
    EventoSerializer,
    ParticipanteSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError

# Permiso para solo lectura o acceso completo para superusuarios
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_superuser

# Permiso para gestionar solo los propios registros como participante
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.correo == request.user.email

# Configuración de paginación personalizada
class ParticipantePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

# ViewSet para Categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminOrReadOnly]

# ViewSet para Eventos
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        categoria_id = self.request.query_params.get('categoria', None)
        fecha = self.request.query_params.get('fecha', None)

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        
        return queryset

    @action(detail=True, methods=['get'], url_path='participantes')
    def listar_participantes(self, request, pk=None):
        evento = self.get_object()
        participantes = evento.participantes.all()
        nombres = [participante.nombre for participante in participantes]
        total = participantes.count()

        return Response({
            'evento': evento.titulo,
            'total_participantes': total,
            'nombres_participantes': nombres
        })

# ViewSet para Participantes
class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre']  # Habilitar búsqueda por nombre
    ordering_fields = ['nombre', 'evento']  # Permitir ordenamiento
    pagination_class = ParticipantePagination  # Configurar paginación

    def get_queryset(self):
        queryset = super().get_queryset()
        evento = self.request.query_params.get('evento')

        # Filtrar por evento si el parámetro está presente
        if evento:
            queryset = queryset.filter(evento_id=evento)

        return queryset

    def perform_create(self, serializer):
        """
        Crear un participante utilizando datos proporcionados desde el frontend
        cuando es un superusuario. Si no, utiliza los datos del usuario autenticado.
        """
        if self.request.user.is_superuser:
            serializer.save()  # Permitir al superusuario enviar todos los datos
        else:
            evento = serializer.validated_data.get('evento')
            correo = self.request.user.email

            if Participante.objects.filter(evento=evento, correo=correo).exists():
                raise ValidationError("Ya estás inscrito en este evento.")

            serializer.save(
                nombre=self.request.user.username,
                correo=self.request.user.email
            )

    def destroy(self, request, *args, **kwargs):
        participante = self.get_object()
        if participante.correo != request.user.email and not request.user.is_superuser:
            return Response(
                {"detail": "No tienes permiso para eliminar este registro."},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(participante)
        return Response({"detail": "Te has desinscrito del evento con éxito."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario registrado con éxito."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
def eventos_inscritos(request):
    inscritos = Participante.objects.filter(correo=request.user.email)
    eventos = [inscrito.evento for inscrito in inscritos]
    serializer = EventoSerializer(eventos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def listar_usuarios(request):
    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data, status=200)
