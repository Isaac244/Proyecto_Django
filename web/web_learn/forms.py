from django import forms
from web_learn.models import Producto

class DocumentForm(forms.ModelForm):
    prod = forms.CharField(
        label="Nombre del Producto"
    )

    class Meta:
        model = Producto
        fields = ("prod",)