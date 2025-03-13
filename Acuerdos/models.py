from django.db import models
from django.utils.crypto import get_random_string
from usuarios.models import User, Unid_Org, Categoria


class Acuerdo(models.Model):
    ESTADOS = [
        ('Archivado', 'Archivado'),
        ('Cumplida', 'Cumplida'),
        ('Espera', 'Espera'),
        ('Incumplida', 'Incumplida'),
        ('Confección', 'Confección'),
        ('Proceso', 'Proceso'),
    ]

    PROCESOS = [
        ('Chequeo diario', 'Chequeo diario'),
        ('Operaciones', 'Operaciones'),
        ('Seguridad y protección', 'Seguridad y protección'),
        ('Inversiones', 'Inversiones'),
        ('Comercial', 'Comercial'),
        ('Logística y servicios', 'Logística y servicios'),
        ('Otro', 'Otro'),
    ]

    codigo = models.CharField(max_length=10, unique=True, editable=False)
    titulo = models.CharField(max_length=200)
    fecha_emision = models.DateField()
    fecha_cumplimiento = models.DateField()
    emisor = models.ForeignKey(
        User, related_name='acuerdos_emisor', on_delete=models.CASCADE)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    procedencia = models.ForeignKey(
        Unid_Org, on_delete=models.SET_NULL, null=True, blank=True)
    responsable = models.ForeignKey(
        User, related_name='acuerdos_responsable', on_delete=models.CASCADE)
    proceso = models.CharField(max_length=50, choices=PROCESOS)
    participantes = models.ManyToManyField(
        User, related_name='acuerdos_participantes', blank=True)
    con_copia = models.ManyToManyField(
        User, related_name='acuerdos_con_copia', blank=True)
    contenido = models.TextField()
    adjunto = models.FileField(upload_to='adjuntos/', blank=True, null=True)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='Confección')

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
