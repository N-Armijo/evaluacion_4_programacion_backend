from rest_framework import serializers
from .models import Categoria, Evento, Participante

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ['id', 'nombre', 'correo', 'evento']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']

        # Si no es superusuario, ocultar el correo
        if not request.user.is_superuser:
            representation.pop('correo', None)

        return representation