from rest_framework import serializers
from .models import Categoria, Evento, Participante
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        # Los campos 'nombre' y 'correo' no deben ser solo de lectura
        # para permitir que el frontend los proporcione.
        extra_kwargs = {
            'nombre': {'required': True},
            'correo': {'required': True}
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

    def create(self, validated_data):
        """
        Utiliza los datos proporcionados por el frontend.
        """
        return super().create(validated_data)


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
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar el campo `is_superuser` al payload del token
        token['is_superuser'] = user.is_superuser
        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Agregar los campos requeridos
