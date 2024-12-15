# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Categoria, Evento, Participante
from .serializers import CategoriaSerializer, EventoSerializer, ParticipanteSerializer

# Create your views here.
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

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


