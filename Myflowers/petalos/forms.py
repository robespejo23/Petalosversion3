from django import forms
from django.forms import ModelForm
from .models import Flores


class FloresForm(ModelForm):
    class meta :
        model = Flores
        fields = [ 'name', 'imagen', 'valor', 'descripcion', 'estado', 'stock']