from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Unid_Org(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    siglas = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.nombre


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('viewer', 'Visualizador')
    ])
    unidad = models.ForeignKey(
        Unid_Org, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Unid_Org
    es_emisor = models.BooleanField(default=False)
    es_responsable = models.BooleanField(default=False)
    es_con_copia = models.BooleanField(default=False)
    es_participante = models.BooleanField(default=False)


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Emisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Responsable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ConCopia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Participante(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
