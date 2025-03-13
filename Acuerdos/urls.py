from django.urls import path
from . import views

urlpatterns = [
    path('crear_acuerdo/', views.crear_acuerdo, name='crear_acuerdo'),
    path('listar_acuerdos/', views.listar_acuerdos, name='listar_acuerdos'),
    path('acuerdos_resp/', views.acuerdos_resp, name='acuerdos_resp'),
    path('editar/<int:id>/', views.editar_acuerdo, name='Editar'),
    path('eliminar/<int:id>/', views.eliminar_acuerdo, name='Eliminar'),
    path('archivar/<int:id>/', views.archivar_acuerdo, name='Archivar'),
    path('cumplir/<int:id>/', views.cumplir_acuerdo, name='Cumplido'),
    path('acuerdo/<int:id>/',
         views.mostrar_acuerdo, name='mostrar_acuerdo'),
    path('documento/<int:id>/', views.documento, name='Documento'),
    path('reasignar/<int:id>/', views.Reasignar_acuerdo.as_view(), name='Reasignar'),
    path('prorrogar/<int:id>/', views.Prorrogar_Acuerdo.as_view(), name='Prorrogar'),
    path('reenviar_correo/<int:id>/',
         views.reenviar_correo, name='Reenviar Correo'),
]
