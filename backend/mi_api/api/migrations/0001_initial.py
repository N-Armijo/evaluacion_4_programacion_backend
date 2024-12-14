# Generated by Django 5.1.4 on 2024-12-14 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('ubicacion', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='api.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participantes', to='api.evento')),
            ],
        ),
    ]