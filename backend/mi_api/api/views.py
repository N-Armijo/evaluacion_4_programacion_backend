from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework import status
from .models import Categoria, Evento, Participante
from .serializers import CategoriaSerializer, EventoSerializer, ParticipanteSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError




# Permiso para solo lectura o acceso completo para superusuarios
class IsAdminOrReadOnly(BasePermission):
    """
    Permite acceso de solo lectura para usuarios regulares. Escritura solo para superusuarios.
    """
    def has_permission(self, request, view):
        # Métodos seguros permitidos para todos
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Métodos de escritura permitidos solo a superusuarios
        return request.user.is_superuser


# Permiso para gestionar solo los propios registros como participante
class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso total a superusuarios. Usuarios regulares solo pueden gestionar sus propios registros.
    """
    def has_object_permission(self, request, view, obj):
        # Superusuarios tienen acceso completo
        if request.user.is_superuser:
            return True
        # Usuarios regulares solo pueden acceder a sus propios registros
        return obj.correo == request.user.email


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
        """
        Lista los nombres de los participantes de un evento y el total de inscritos.
        """
        evento = self.get_object()  # Obtener el evento actual por ID
        participantes = evento.participantes.all()  # Obtener los participantes relacionados
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

    def perform_create(self, serializer):
        """
        Inscribe al usuario autenticado en un evento, evitando duplicados.
        """
        evento = serializer.validated_data.get('evento')
        correo = self.request.user.email

        if Participante.objects.filter(evento=evento, correo=correo).exists():
            raise ValidationError("Ya estás inscrito en este evento.")

        serializer.save(
            nombre=self.request.user.username,
            correo=self.request.user.email
        )




# Endpoint para registrar usuarios
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def register_user(request):
    """
    Endpoint para registrar nuevos usuarios.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario registrado con éxito."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer