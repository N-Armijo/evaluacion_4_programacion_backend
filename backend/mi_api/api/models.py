from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"

class Participante(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="participantes")

    def __str__(self):
        return f"{self.nombre} ({self.evento.titulo})"