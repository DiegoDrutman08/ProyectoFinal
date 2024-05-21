from django import forms
from . import models
from .models import UserProfile

class LocalidadForm(forms.ModelForm):
    class Meta:
        model = models.Localidad
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = models.Sucursal
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "localidad_id": forms.Select(attrs={"class": "form-control"}),
            "fecha_actualizacion": forms.TextInput(attrs={"class": "form-control"}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nombre', 'direccion', 'avatar']

