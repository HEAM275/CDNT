from django.urls import path
from . import views

urlpatterns = [
    path('acuerdos/', views.estadisticas_acuerdos, name='acuerdos_por_estado'),
    path('acuerdos_por_proceso/', views.estadisticas_acuerdo_proceso,
         name='estadisticas_acuerdo_proceso'),
    path('indicaciones/', views.estadisticas_indicaciones,
         name='indicaciones_por_estado'),
    path('indicaciones_por_proceso/', views.estadisticas_indicaciones_proceso,
         name='indicaciones_por_proceso'),
]
