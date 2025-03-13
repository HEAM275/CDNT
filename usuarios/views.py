from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User, Categoria, Unid_Org, Emisor, Responsable, ConCopia, Participante
from .forms import UserForm, CategoriaForm, Unid_OrgForm, EditarRolesForm

# Create your views here.


def home(request):
    return render(request, 'home.html', )


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('principal')


@login_required
def principal(request):
    return render(request, 'principal.html')


@login_required
def salir(request):
    logout(request)
    return redirect('home')


@login_required
def gestUser(request):
    usuarios = User.objects.all()
    return render(request, 'gestuser.html', {'usuarios': usuarios})


@login_required
def crear_user(request):
    if request.method == 'GET':
        return render(request, 'crear_user.html', {
            'form': UserForm
        })
    else:
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'principal.html', {
                'form': UserForm
            })
        else:
            return render(request, 'crear_user.html', {
                'form': UserForm,
                'error': 'formulario no válido, complete los campos correctamente'
            })


@login_required
def eliminarU(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        user.delete()
        messages.success(request, f'Usuario {
                         username}) eliminado correctamente.')
        return redirect('gestion_de_usuario')
    return redirect('gestion_de_usuario')


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirige a la página de gestión de usuarios
            return redirect('gestion_de_usuario')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'gest_cate.html', {'categorias': categorias})


@login_required
@user_passes_test(lambda u: u.is_staff)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gest_cate')
    else:
        form = CategoriaForm()
    return render(request, 'categoria_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('gest_cate')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('gest_cate')
    return render(request, 'categoria_confirm_delete.html', {'object': categoria})


@login_required
def gestion_unidades(request):
    unidades = Unid_Org.objects.all()
    if request.method == 'POST':
        form = Unid_OrgForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_unidades')
    else:
        form = Unid_OrgForm()
    return render(request, 'gestion_unidades.html', {'unidades': unidades, 'form': form})


@login_required
def unidad_create(request):
    if request.method == 'POST':
        form = Unid_OrgForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_unidades')
    else:
        form = Unid_OrgForm()
    return render(request, 'unidad_form.html', {'form': form})


@login_required
def editar_unidad(request, pk):
    unidad = get_object_or_404(Unid_Org, pk=pk)
    if request.method == 'POST':
        form = Unid_OrgForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('gestion_unidades')
    else:
        form = Unid_OrgForm(instance=unidad)
    return render(request, 'unidad_form.html', {'form': form})


@login_required
def eliminar_unidad(request, pk):
    unidad = get_object_or_404(Unid_Org, pk=pk)
    unidad.delete()
    return redirect('gestion_unidades')


EditarRolesFormSet = modelformset_factory(User, form=EditarRolesForm, extra=0)


@login_required
def gestion_roles(request):
    EditarRolesFormSet = modelformset_factory(User, fields=(
        'id', 'username', 'es_emisor', 'es_responsable', 'es_con_copia', 'es_participante'), extra=0)

    if request.method == 'POST':
        formset = EditarRolesFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
                actualizar_tablas_roles(instance)
            return redirect('principal')
    else:
        formset = EditarRolesFormSet(queryset=User.objects.all())

    return render(request, 'gestion_roles.html', {'formset': formset})


def actualizar_tablas_roles(usuario):
    if usuario.es_emisor:
        Emisor.objects.get_or_create(user=usuario)
    else:
        Emisor.objects.filter(user=usuario).delete()

    if usuario.es_responsable:
        Responsable.objects.get_or_create(user=usuario)
    else:
        Responsable.objects.filter(user=usuario).delete()

    if usuario.es_con_copia:
        ConCopia.objects.get_or_create(user=usuario)
    else:
        ConCopia.objects.filter(user=usuario).delete()

    if usuario.es_participante:
        Participante.objects.get_or_create(user=usuario)
    else:
        Participante.objects.filter(user=usuario).delete()
