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
from .forms import IndicacionForm
from .models import Indicacion
from usuarios.models import User
import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def crear_indicacion(request):
    if request.method == 'POST':
        form = IndicacionForm(request.POST, request.FILES)
        if form.is_valid():
            indicacion = form.save(commit=False)
            action = request.POST.get('action')
            if action == 'guardar':
                indicacion.estado = 'Confección'
                indicacion.save()
                return redirect('listar_indicacion')
            elif action == 'enviar':
                indicacion.estado = 'Proceso'
                indicacion.save()
                enviar_correo(indicacion)
                return redirect('listar_indicacion')
        else:
            print(form.errors)  # Imprime errores del formulario si no es válido
    else:
        form = IndicacionForm()
    return render(request, 'crear_indicacion.html', {'form': form})


def enviar_correo(indicacion):
    asunto = f'Nueva Indicacion: {indicacion.titulo}'
    mensaje = f"""
        Se ha creado un nuevo indicacion.
        Título: {indicacion.titulo}
        Emisor: {indicacion.emisor}
        Fecha de Emisión: {indicacion.fecha_emision}
        Fecha de Cumplimiento: {indicacion.fecha_cumplimiento}
        Contenido: {indicacion.contenido}
    """
    destinatarios = list(indicacion.participantes.all().values_list(
        'email', flat=True)) + list(indicacion.con_copia.all().values_list('email', flat=True))
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, destinatarios)


@login_required
def listar_indicacion(request):
    indicaciones = Indicacion.objects.all().order_by('fecha_emision')
    paginator = Paginator(indicaciones, 7)

    for indicacion in indicaciones:
        if indicacion.fecha_cumplimiento and indicacion.fecha_emision:
            indicacion.dias = (indicacion.fecha_cumplimiento -
                               indicacion.fecha_emision).days
        else:
            indicacion.dias = None

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_indicacion.html', {'page_obj': page_obj})


@login_required
def indicaciones_resp(request):

    usuario_actual = request.user

    indicaciones = Indicacion.objects.filter(
        responsable=usuario_actual).order_by('fecha_emision')
    paginator = Paginator(indicaciones, 7)

    for indicacion in indicaciones:
        if indicacion.fecha_cumplimiento and indicacion.fecha_emision:
            indicacion.dias = (indicacion.fecha_cumplimiento -
                               indicacion.fecha_emision).days
        else:
            indicacion.dias = None

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_indicacion.html', {'page_obj': page_obj})


@login_required
def eliminar_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    indicacion.delete()
    # Redirige a la lista de acuerdos después de eliminar
    return redirect('listar_indicacion')


@login_required
def editar_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    if request.method == 'POST':
        form = IndicacionForm(request.POST, instance=indicacion)
        if form.is_valid():
            indicacion = form.save(commit=False)
            indicacion.estado = 'Espera'
            indicacion.save()
            return redirect('listar_indicacion')
    else:
        form = IndicacionForm(instance=indicacion)
    return render(request, 'editar_indicacion.html', {'form': form})


@login_required
def cumplir_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    indicacion.estado = 'Cumplido'
    indicacion.save()
    return redirect('listar_indicacion')


@login_required
def archivar_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    indicacion.estado = 'Archivado'
    indicacion.save()
    return redirect('listar_indicacion')


ACCIONES_POR_ESTADO = {
    'Archivado': ['Documento'],
    'Cumplido': ['Documento', 'Archivar'],
    'Espera': ['Documento', 'Cumplido'],
    'Confección': ['Documento', 'Editar', 'Eliminar'],
    'Incumplido': ['Documento',  'Reasignar', 'Prorrogar', 'Cumplido', 'Reenviar Correo'],
    'Proceso': ['Documento', 'Reasignar', 'Prorrogar', 'Cumplido', 'Reenviar Correo'],
}


@login_required
def mostrar_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    acciones = ACCIONES_POR_ESTADO.get(indicacion.estado, [])
    acciones_urls = {accion: reverse(f"{accion.lower()}_indicacion", args=[
                                     id]) for accion in acciones}
    return render(request, 'indicacion_detalle.html', {'indicacion': indicacion, 'acciones_urls': acciones_urls})


class Reasignar_indicacion(View):
    template_name = 'edit_resp.html'

    def get(self, request, id):
        indicacion = get_object_or_404(Indicacion, id=id)
        form = IndicacionForm(instance=indicacion)

        # Deshabilitar todos los campos excepto 'responsable'
        for field in form.fields:
            if field != 'responsable':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'indicacion': indicacion})

    def post(self, request, id):
        indicacion = get_object_or_404(Indicacion, id=id)
        post_data = request.POST.copy()

        # Convertir el ID en una instancia de User
        if 'responsable' in post_data:
            responsable_id = post_data['responsable']
            responsable_instance = get_object_or_404(User, id=responsable_id)
            indicacion.responsable = responsable_instance
            indicacion.save()
            return redirect('listar_indicacion')

        form = IndicacionForm(instance=indicacion)
        for field in form.fields:
            if field != 'responsable':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'indicacion': indicacion})


class Prorrogar_indicacion(View):
    template_name = 'prorrogar_indicacion.html'

    def get(self, request, id):
        indicacion = get_object_or_404(Indicacion, id=id)
        form = IndicacionForm(instance=indicacion)

        # Deshabilitar todos los campos excepto 'fecha_cumplimiento'
        for field in form.fields:
            if field != 'fecha_cumplimiento':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'indicacion': indicacion})

    def post(self, request, id):
        hoy = timezone.now().date()
        indicacion = get_object_or_404(Indicacion, id=id)
        post_data = request.POST.copy()

        # Actualiza solo el campo 'fecha_cumplimiento'
        if 'fecha_cumplimiento' in post_data:
            try:
                fecha_cumplimiento = datetime.datetime.strptime(
                    post_data['fecha_cumplimiento'], '%Y-%m-%d').date()
            except ValueError:
                form = IndicacionForm(instance=indicacion)
                for field in form.fields:
                    if field != 'fecha_cumplimiento':
                        form.fields[field].widget.attrs['disabled'] = 'disabled'
                return render(request, self.template_name, {'form': form, 'indicacion': indicacion, 'error': 'Fecha inválida'})

            indicacion.fecha_cumplimiento = fecha_cumplimiento
            if indicacion.fecha_cumplimiento and indicacion.fecha_cumplimiento > hoy:
                indicacion.estado = 'Confección'
            indicacion.save()
            return redirect('listar_indicacion')

        form = IndicacionForm(instance=indicacion)
        for field in form.fields:
            if field != 'fecha_cumplimiento':
                form.fields[field].widget.attrs['disabled'] = 'disabled'

        return render(request, self.template_name, {'form': form, 'indicacion': indicacion})


# Ruta al ejecutable de wkhtmltopdf
# Ajusta esta ruta según tu sistema operativo
path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


@login_required
def documento_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    if request.method == 'POST':
        # Lógica para generar el PDF
        context = {'indicacion': indicacion}
        html = render_to_string('Indicaciones/pdf_template.html', context)
        pdf = pdfkit.from_string(html, False, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="indicacion.pdf"'
        return response

    return render(request, 'documento_indicacion.html', {'indicacion': indicacion})


def reenviar_correo_indicacion(request, id):
    indicacion = get_object_or_404(Indicacion, id=id)
    enviar_correo(indicacion)
    return redirect('principal')
