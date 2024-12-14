# from django.shortcuts import render
from rest_framework import viewsets
from .models import Categoria, Evento, Participante
from .serializers import CategoriaSerializer, EventoSerializer, ParticipanteSerializer

# Create your views here.
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

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

