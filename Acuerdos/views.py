from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
import datetime
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .forms import AcuerdoForm
from .models import Acuerdo
from usuarios.models import User
from django.contrib.auth.decorators import login_required
import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.


@login_required
def crear_acuerdo(request):
    if request.method == 'POST':
        form = AcuerdoForm(request.POST, request.FILES)
        if form.is_valid():
            acuerdo = form.save(commit=False)
            action = request.POST.get('action')
            if action == 'guardar':
                acuerdo.estado = 'Confección'
                acuerdo.save()
                return redirect('listar_acuerdos')
            elif action == 'enviar':
                acuerdo.estado = 'Proceso'
                acuerdo.save()
                enviar_correo(acuerdo)
                return redirect('listar_acuerdos')
        else:
            print(form.errors)  # Imprime errores del formulario si no es válido
    else:
        form = AcuerdoForm()
    return render(request, 'crear_acuerdo.html', {'form': form})


def enviar_correo(acuerdo):
    asunto = f'Nuevo Acuerdo: {acuerdo.titulo}'
    mensaje = f"""
        Se ha creado un nuevo acuerdo.
        Título: {acuerdo.titulo}
        Emisor: {acuerdo.emisor}
        Fecha de Emisión: {acuerdo.fecha_emision}
        Fecha de Cumplimiento: {acuerdo.fecha_cumplimiento}
        Contenido: {acuerdo.contenido}
    """
    destinatarios = list(acuerdo.participantes.all().values_list(
        'email', flat=True)) + list(acuerdo.con_copia.all().values_list('email', flat=True))
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, destinatarios)


@login_required
def listar_acuerdos(request):
    acuerdos = Acuerdo.objects.all().order_by('fecha_emision')
    paginator = Paginator(acuerdos, 7)

    for acuerdo in acuerdos:
        if acuerdo.fecha_cumplimiento and acuerdo.fecha_emision:
            acuerdo.dias = (acuerdo.fecha_cumplimiento -
                            acuerdo.fecha_emision).days
        else:
            acuerdo.dias = None

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_acuerdos.html', {'page_obj': page_obj})


@login_required
def acuerdos_resp(request):

    usuario_actual = request.user

    acuerdos = Acuerdo.objects.filter(
        responsable=usuario_actual).order_by('fecha_emision')
    paginator = Paginator(acuerdos, 7)

    for acuerdo in acuerdos:
        if acuerdo.fecha_cumplimiento and acuerdo.fecha_emision:
            acuerdo.dias = (acuerdo.fecha_cumplimiento -
                            acuerdo.fecha_emision).days
        else:
            acuerdo.dias = None

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_acuerdos.html', {'page_obj': page_obj})


@login_required
def eliminar_acuerdo(request, id):
    acuerdo = get_object_or_404(Acuerdo, id=id)
    acuerdo.delete()
    # Redirige a la lista de acuerdos después de eliminar
    return redirect('listar_acuerdos')


@login_required
def editar_acuerdo(request, id):
    acuerdo = get_object_or_404(Acuerdo, id=id)
    if request.method == 'POST':
        form = AcuerdoForm(request.POST, instance=acuerdo)
        if form.is_valid():
            acuerdo = form.save(commit=False)
            acuerdo.estado = 'Espera'
            acuerdo.save()
            return redirect('listar_acuerdos')
    else:
        form = AcuerdoForm(instance=acuerdo)
    return render(request, 'editar_acuerdo.html', {'form': form})


@login_required
def cumplir_acuerdo(request, id):
    acuerdo = get_object_or_404(Acuerdo, id=id)
    acuerdo.estado = 'Cumplido'
    acuerdo.save()
    return redirect('listar_acuerdos')


@login_required
def archivar_acuerdo(request, id):
    acuerdo = get_object_or_404(Acuerdo, id=id)
    acuerdo.estado = 'Archivado'
    acuerdo.save()
    return redirect('listar_acuerdos')


# archivar , cumplido , editar, eliminar,reasignar,
# documento,expediente,observacion,revisar resumen,prorrogar,reenviar correo
ACCIONES_POR_ESTADO = {
    'Archivado': ['Documento'],
    'Cumplido': ['Documento', 'Archivar'],
    'Espera': ['Documento', 'Cumplido'],
    'Confección': ['Documento', 'Editar', 'Eliminar'],
    'Incumplido': ['Documento',  'Reasignar', 'Prorrogar', 'Cumplido', 'Reenviar Correo'],
    'Proceso': ['Documento', 'Reasignar', 'Prorrogar', 'Cumplido', 'Reenviar Correo'],
}


@login_required
def mostrar_acuerdo(request, id):
    acuerdo = Acuerdo.objects.get(id=id)
    acciones = ACCIONES_POR_ESTADO.get(acuerdo.estado, [])
    return render(request, 'acuerdo_detalle.html', {'acuerdo': acuerdo, 'acciones': acciones})


path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


@login_required
def documento(request, id):
    acuerdo = get_object_or_404(Acuerdo, id=id)
    if request.method == 'POST':
        context = {'acuerdo': acuerdo}
        html = render_to_string('Acuerdos/pdf_template.html', context)
        pdf = pdfkit.from_string(html, False, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename:"acuerdo.pdf"'
        return response

    return render(request, 'documento_acuerdo.html', {'acuerdo': acuerdo})


class Reasignar_acuerdo(View):
    template_name = 'edit_respon.html'

    def get(self, request, id):
        acuerdo = get_object_or_404(Acuerdo, id=id)
        form = AcuerdoForm(instance=acuerdo)

        # Deshabilitar todos los campos excepto 'responsable'
        for field in form.fields:
            if field != 'responsable':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'acuerdo': acuerdo})

    def post(self, request, id):
        acuerdo = get_object_or_404(Acuerdo, id=id)
        post_data = request.POST.copy()

        # Convertir el ID en una instancia de User
        if 'responsable' in post_data:
            responsable_id = post_data['responsable']
            responsable_instance = get_object_or_404(User, id=responsable_id)
            acuerdo.responsable = responsable_instance
            acuerdo.save()
            return redirect('listar_acuerdos')

        form = AcuerdoForm(instance=acuerdo)
        for field in form.fields:
            if field != 'responsable':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'acuerdo': acuerdo})


class Prorrogar_Acuerdo(View):
    template_name = 'prorrogar_acuerdo.html'

    def get(self, request, id):
        acuerdo = get_object_or_404(Acuerdo, id=id)
        form = AcuerdoForm(instance=acuerdo)

        # Deshabilitar todos los campos excepto 'fecha_cumplimiento'
        for field in form.fields:
            if field != 'fecha_cumplimiento':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'acuerdo': acuerdo})

    def post(self, request, id):
        hoy = timezone.now().date()
        acuerdo = get_object_or_404(Acuerdo, id=id)
        post_data = request.POST.copy()

        # Actualiza solo el campo 'fecha_cumplimiento'
        if 'fecha_cumplimiento' in post_data:
            try:
                fecha_cumplimiento = datetime.datetime.strptime(
                    post_data['fecha_cumplimiento'], '%Y-%m-%d').date()
            except ValueError:
                form = AcuerdoForm(instance=acuerdo)
                for field in form.fields:
                    if field != 'fecha_cumplimiento':
                        form.fields[field].widget.attrs['disabled'] = 'disabled'
                return render(request, self.template_name, {'form': form, 'acuerdo': acuerdo, 'error': 'Fecha inválida'})

            acuerdo.fecha_cumplimiento = fecha_cumplimiento
            if acuerdo.fecha_cumplimiento and acuerdo.fecha_cumplimiento > hoy:
                acuerdo.estado = 'Confección'
            acuerdo.save()
            return redirect('listar_acuerdos')

        form = AcuerdoForm(instance=acuerdo)
        for field in form.fields:
            if field != 'fecha_cumplimiento':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'acuerdo': acuerdo})


def reenviar_correo(request, id):
    acuerdo = get_object_or_404(Acuerdo, id=id)
    enviar_correo(acuerdo)
    return redirect('principal')
