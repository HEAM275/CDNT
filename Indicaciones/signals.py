from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import Indicacion


@receiver(user_logged_in)
def verificar_y_actualizar_estados(sender, user, request, **kwargs):
    hoy = timezone.now().date()
    indicaciones = Indicacion.objects.exclude(
        estado__in=['Cumplida', 'Archivado'])
    for indicacion in indicaciones:
        if indicacion.fecha_cumplimiento and indicacion.fecha_cumplimiento < hoy:
            indicacion.estado = 'Incumplido'
            indicacion.save()
