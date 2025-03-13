from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import Acuerdo


@receiver(user_logged_in)
def verificar_y_actualizar_estados(sender, user, request, **kwargs):
    hoy = timezone.now().date()
    acuerdos = Acuerdo.objects.exclude(estado__in=['Cumplido', 'Archivado'])
    for acuerdo in acuerdos:
        if acuerdo.fecha_cumplimiento and acuerdo.fecha_cumplimiento < hoy:
            acuerdo.estado = 'Incumplido'
            acuerdo.save()
