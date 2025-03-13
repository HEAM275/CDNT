from django.urls import path
from . import views

urlpatterns = [
    path('crear_indicacion/', views.crear_indicacion, name='crear_indicacion'),
    path('listar_indicacion/', views.listar_indicacion, name='listar_indicacion'),
    path('indicaciones_resp/', views.indicaciones_resp, name='indicaciones_resp'),
    path('editar/<int:id>/', views.editar_indicacion, name='editar_indicacion'),
    path('eliminar/<int:id>/', views.eliminar_indicacion,
         name='eliminar_indicacion'),
    path('archivar/<int:id>/', views.archivar_indicacion,
         name='archivar_indicacion'),
    path('cumplir/<int:id>/', views.cumplir_indicacion,
         name='cumplido_indicacion'),
    path('indicacion/<int:id>/', views.mostrar_indicacion,
         name='mostrar_indicacion'),
    path('documento/<int:id>/', views.documento_indicacion,
         name='documento_indicacion'),  # Agregar esta línea
    path('reasignar/<int:id>/', views.Reasignar_indicacion.as_view(),
         name='reasignar_indicacion'),
    path('prorrogar/<int:id>/', views.Prorrogar_indicacion.as_view(),
         name='prorrogar_indicacion'),
    path('reenviar_correo/<int:id>/', views.reenviar_correo_indicacion,
         name='reenviar correo_indicacion'),

]
