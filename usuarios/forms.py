from django.forms import ModelForm
from django import forms
from .models import User, Categoria, Unid_Org


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'password', 'first_name',
            'last_name', 'email', 'phone_number', 'role', 'unidad'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su usuario'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su contraseña'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba sus apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su correo electronico'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba su numero de teléfono'}),
            'role': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Asigne el rol deseado'}),
            'unidad': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Asigne la unidad a la que pertenece'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']


class Unid_OrgForm(forms.ModelForm):
    class Meta:
        model = Unid_Org
        fields = ['nombre', 'siglas']


class EditarRolesForm(forms.ModelForm):
    es_emisor = forms.BooleanField(required=False)
    es_responsable = forms.BooleanField(required=False)
    es_con_copia = forms.BooleanField(required=False)
    es_participante = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['es_emisor', 'es_responsable',
                  'es_con_copia', 'es_participante']
