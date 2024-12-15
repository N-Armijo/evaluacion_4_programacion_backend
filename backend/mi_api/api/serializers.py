from rest_framework import serializers
from .models import Categoria, Evento, Participante
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

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
        extra_kwargs = {
            'nombre': {'error_messages': {'blank': "El nombre no puede estar vacío."}},
            'correo': {'error_messages': {'blank': "El correo no puede estar vacío."}},
            'evento': {'error_messages': {'null': "Debe especificar un evento válido."}}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']

        # Si no es superusuario, ocultar el correo
        if not request.user.is_superuser:
            representation.pop('correo', None)

        return representation
    
    def validate(self, data):
        # Validar que un usuario no se registre dos veces en el mismo evento
        evento = data.get('evento')
        correo = data.get('correo')

        if Participante.objects.filter(evento=evento, correo=correo).exists():
            raise ValidationError("Este usuario ya está registrado en el evento.")
        
        return data

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Crea un nuevo usuario con los datos validados.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user