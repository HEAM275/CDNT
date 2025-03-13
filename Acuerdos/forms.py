from django import forms
from .models import Acuerdo
from usuarios.models import User, Categoria, Unid_Org


class AcuerdoForm(forms.ModelForm):
    fecha_emision = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    fecha_cumplimiento = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Acuerdo
        fields = ['titulo', 'fecha_emision', 'fecha_cumplimiento', 'emisor', 'categoria',
                  'procedencia', 'responsable', 'proceso', 'participantes', 'con_copia', 'contenido', 'adjunto']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'emisor': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'procedencia': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'proceso': forms.Select(attrs={'class': 'form-select'}),
            'participantes': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'con_copia': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'adjunto': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emisor'].queryset = User.objects.filter(es_emisor=True)
        self.fields['responsable'].queryset = User.objects.filter(
            es_responsable=True)
        self.fields['participantes'].queryset = User.objects.filter(
            es_participante=True)
        self.fields['con_copia'].queryset = User.objects.filter(
            es_con_copia=True)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['procedencia'].queryset = Unid_Org.objects.all()
