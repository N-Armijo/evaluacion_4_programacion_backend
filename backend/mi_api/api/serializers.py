from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria, Evento, Participante
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializer personalizado para Token JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

# Serializer para Usuarios
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['', 'username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password']
#         )
#         return user
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username','password', 'email' ]

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

# Serializer para Categorías
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# Serializer para Eventos
class EventoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'

# Serializer para Participantes
class ParticipanteSerializer(serializers.ModelSerializer):
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)

    class Meta:
        model = Participante
        fields = '__all__'
