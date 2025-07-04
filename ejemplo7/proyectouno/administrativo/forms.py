from django.forms import ModelForm
from django import forms

from administrativo.models import *

class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        fields = ['estudiante', 'modulo', 'comentario']



class MatriculaEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MatriculaEditForm, self).__init__(*args, **kwargs)
        self.initial['estudiante'] = self.instance.estudiante
        self.fields["estudiante"].widget = forms.widgets.HiddenInput()
        self.initial['modulo'] = self.instance.modulo
        self.fields["modulo"].widget = forms.widgets.HiddenInput()

    class Meta:
        model = Matricula
        fields = ['estudiante', 'modulo', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': 'Escribe aquí tu comentario...'
            }),}


class ModuloForm(forms.ModelForm):
        class Meta:
            model = Modulo
            fields = ['nombre', 'valor']
class EstudianteForm(forms.ModelForm):
        class Meta:
            model = Estudiante
            fields = ['nombre', 'apellido', 'cedula', 'edad', 'tipo_estudiante']
