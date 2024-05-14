from django import forms
from . import models

class ProductoCategoriaForm(forms.ModelForm):
    class Meta:
        model = models.ProductoCategoria
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "unidad_medida": forms.TextInput(attrs={"class": "form-control"}),
            "precio": forms.TextInput(attrs={"class": "form-control"}),
            "categoria_id": forms.Select(attrs={"class": "form-control"}),
            "fecha_actualizacion": forms.TextInput(attrs={"class": "form-control"}),
        }