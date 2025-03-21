from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Acuerdos.models import Acuerdo
from Indicaciones.models import Indicacion
import matplotlib.pyplot as plt
import io
import urllib
import base64

# funcion generadora de graficos


def generar_grafico_pastel(datos, colores, etiquetas):
    # Verifica si todos los datos son 0 o si la lista está vacía
    if all(d == 0 for d in datos) or not datos:
        # Crear un gráfico vacío con un mensaje
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No hay datos disponibles',
                horizontalalignment='center', verticalalignment='center',
                fontsize=12, color='gray')
        ax.axis('off')  # Oculta los ejes
    else:
        # Generar el gráfico de pastel normal
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(datos, labels=etiquetas, colors=colores,
                                          autopct='%1.1f%%', startangle=90,
                                          wedgeprops={'linewidth': 1, 'edgecolor': 'black'})

        # Aseguramos que solo la sección blanca tenga borde negro
        for i, wedge in enumerate(wedges):
            if colores[i] == 'white':
                wedge.set_edgecolor('black')

        ax.axis('equal')  # Asegura que el gráfico sea un círculo

        plt.setp(autotexts, size=10, weight="bold", color="black")
        plt.setp(texts, size=10, weight="bold")

    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    grafico_base64 = base64.b64encode(image_png).decode('utf-8')
    plt.close()  # Cierra la figura para liberar memoria
    return grafico_base64


@login_required
def estadisticas_acuerdos(request):
    acuerdos = Acuerdo.objects.all()
    estados = ['Archivado', 'Cumplido', 'Espera',
               'Incumplido', 'Confección', 'Proceso']
    colores = ['orange', 'blue', 'pink', 'red', 'yellow', 'green']
    datos = [acuerdos.filter(estado=estado).count() for estado in estados]
    grafico_acuerdos = generar_grafico_pastel(datos, colores, estados)
    return render(request, 'estadisticas_acuerdos.html', {'grafico_acuerdos': grafico_acuerdos})


@login_required
def estadisticas_acuerdo_proceso(request):
    acuerdos = Acuerdo.objects.all()
    procesos = ['Chequeo diario', 'Operaciones', 'Seguridad y protección',
                'Inversiones', 'Comercial', 'Logistica y servicios', 'Otro']
    colores = ['green', 'blue', 'red', 'orange', 'yellow', 'purple', 'white']
    datos = [acuerdos.filter(proceso=proceso).count() for proceso in procesos]
    grafico_acuerdos_proceso = generar_grafico_pastel(datos, colores, procesos)
    return render(request, 'estadisticas_acuerdo_proceso.html', {'grafico_acuerdos_proceso': grafico_acuerdos_proceso})


@login_required
def estadisticas_indicaciones(request):
    indicaciones = Indicacion.objects.all()
    estados = ['Archivado', 'Cumplido', 'Espera',
               'Incumplido', 'Confección', 'Proceso']
    colores = ['orange', 'blue', 'pink', 'red', 'yellow', 'green']
    datos = [indicaciones.filter(estado=estado).count() for estado in estados]
    grafico_indicaciones = generar_grafico_pastel(datos, colores, estados)
    return render(request, 'estadisticas_indicaciones.html', {'grafico_indicaciones': grafico_indicaciones})


@login_required
def estadisticas_indicaciones_proceso(request):
    indicaciones = Indicacion.objects.all()
    procesos = ['Chequeo diario', 'Operaciones', 'Seguridad y protección',
                'Inversiones', 'Comercial', 'Logistica y servicios', 'Otro']
    colores = ['green', 'blue', 'red', 'orange', 'yellow', 'purple', 'white']
    datos = [indicaciones.filter(proceso=proceso).count()
             for proceso in procesos]
    grafico_indicaciones_proceso = generar_grafico_pastel(
        datos, colores, procesos)
    return render(request, 'estadisticas_indicaciones_proceso.html', {'grafico_indicaciones_proceso': grafico_indicaciones_proceso})
