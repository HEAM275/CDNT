
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.sign_in, name='signin'),
    path('principal/', views.principal, name='principal'),
    path('logout/', views.salir, name='logout'),
    path('gestion_de_usuario/', views.gestUser, name='gestion_de_usuario'),
    path('crear/user', views.crear_user, name='crear_user'),
    path('del_user/<str:username>', views.eliminarU, name='del_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('gest_cate/', views.categoria_list, name='gest_cate'),
    path('gest_cate/nueva/', views.categoria_create, name='categoria_nueva'),
    path('gest_cate/<int:pk>/editar/',
         views.categoria_update, name='categoria_editar'),
    path('gest_cate/<int:pk>/eliminar/',
         views.categoria_delete, name='categoria_eliminar'),
    path('gestion_unidades/', views.gestion_unidades, name='gestion_unidades'),
    path('nueva_unidad/', views.unidad_create, name='nueva_unidad'),
    path('editar_unidad/<int:pk>/', views.editar_unidad, name='editar_unidad'),
    path('eliminar_unidad/<int:pk>/',
         views.eliminar_unidad, name='eliminar_unidad'),
    path('gestion_roles/', views.gestion_roles, name='gestion_roles'),
]
