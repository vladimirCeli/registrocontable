from django.forms import ModelForm
from .models import Registro
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class primerRegistro(ModelForm):
    class Meta:
        model = Registro
        fields = ['fecha', 'detalle', 'esaldo', 'bsaldo']
        widgets = {'fecha': DateInput()}

class crearRegistroForm(ModelForm):
    class Meta:
        model = Registro
        fields = ['fecha', 'detalle', 'ncomprobante', 'eingresos', 'eegresos', 'esaldo', 'bingresos', 'begresos', 'bsaldo']
        widgets = {'fecha': DateInput()}