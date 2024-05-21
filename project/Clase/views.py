from .models import Sucursal, Cliente, Vendedor, Pedido
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import forms, models
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib import messages
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

def home(request):
    return render(request, "clase/index.html")

class LocalidadList(ListView):
    model = models.Localidad

    def get_queryset(self) -> QuerySet:
        if self.request.GET.get("consulta"):
            consulta = self.request.GET.get("consulta")
            object_list = models.Localidad.objects.filter(nombre__icontains=consulta)
        else:
            object_list = models.Localidad.objects.all()
        return object_list

class LocalidadCreate(CreateView):
    model = models.Localidad
    form_class = forms.LocalidadForm
    success_url = reverse_lazy("clase:home")

class LocalidadUpdate(UpdateView):
    model = models.Localidad
    form_class = forms.LocalidadForm
    success_url = reverse_lazy("clase:localidad_list")

class LocalidadDetail(DetailView):
    model = models.Localidad

class LocalidadDelete(DeleteView):
    model = models.Localidad
    success_url = reverse_lazy("clase:localidad_list")

class SucursalList(ListView):
    model = models.Sucursal

    def get_queryset(self) -> QuerySet:
        if self.request.GET.get("consulta"):
            consulta = self.request.GET.get("consulta")
            object_list = models.Sucursal.objects.filter(nombre__icontains=consulta)
        else:
            object_list = models.Sucursal.objects.all()
        return object_list


class SucursalCreate(CreateView):
    model = models.Sucursal
    form_class = forms.SucursalForm
    success_url = reverse_lazy("clase:home")


class SucursalUpdate(UpdateView):
    model = models.Sucursal
    form_class = forms.SucursalForm
    success_url = reverse_lazy("clase:sucursal_list")


class SucursalDetail(DetailView):
    model = models.Sucursal


class SucursalDelete(DeleteView):
    model = models.Sucursal
    success_url = reverse_lazy("clase:sucursal_list")

def agregar_cliente(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre')
        direccion_cliente = request.POST.get('direccion')
        email_cliente = request.POST.get('email')
        edad_cliente = request.POST.get('edad')

        if Cliente.objects.filter(nombre=nombre_cliente).exists():
            messages.error(request, 'Ya existe un cliente con este nombre')
            return render(request, 'core/index.html', {'mensaje': 'Ya existe un cliente con este nombre'})

        Cliente.objects.create(nombre=nombre_cliente, direccion=direccion_cliente, email=email_cliente, edad=edad_cliente)

        return redirect('clase:agregar_pedido')
    else:
        return render(request, 'core/base.html')
    
def agregar_vendedor(request):
    if request.method == 'POST':
        nombre_vendedor = request.POST.get('vendedor')
        edad_vendedor = request.POST.get('edad')

        if Vendedor.objects.filter(nombre=nombre_vendedor).exists():
            messages.error(request, 'Ya existe un vendedor con este nombre')
            return render(request, 'core/index_staff.html', {'mensaje': 'Ya existe un vendedor con este nombre'})
        
        if nombre_vendedor and edad_vendedor:
            Vendedor.objects.create(nombre=nombre_vendedor, edad=edad_vendedor)
            return redirect('core:home')
        else:
            return render(request, 'core/base.html', {'message': 'El nombre y la edad del vendedor son obligatorios'})
    else:
        return render(request, 'core/base.html')

def agregar_pedido(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        sucursal_id = request.POST.get('sucursales')
        vendedor_id = request.POST.get('vendedores')
        cliente_id = request.POST.get('clientes')
        
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
            vendedor = Vendedor.objects.get(id=vendedor_id)
            cliente = Cliente.objects.get(id=cliente_id)
            
            while Pedido.objects.filter(codigo=codigo).exists():
                messages.error(request, 'Ya existe un pedido con este codigo')
                return render(request, 'core/agregar_pedido.html', {'mensaje': 'Ya existe un pedido con este codigo'})
            
            pedido = Pedido.objects.create(codigo=codigo, sucursal=sucursal, vendedor=vendedor, cliente=cliente)
        except (Sucursal.DoesNotExist, Vendedor.DoesNotExist, Cliente.DoesNotExist):
            error_message = "Uno o más objetos no existen"
            sucursales = Sucursal.objects.all()
            vendedores = Vendedor.objects.all()
            clientes = Cliente.objects.all()
            return render(request, 'core/agregar_pedido.html', {'error_message': error_message, 'sucursales': sucursales, 'vendedores': vendedores, 'clientes': clientes})
        except IntegrityError:
            error_message = "Ya existe un pedido con este código"
            sucursales = Sucursal.objects.all()
            vendedores = Vendedor.objects.all()
            clientes = Cliente.objects.all()
            return render(request, 'core/agregar_pedido.html', {'error_message': error_message, 'sucursales': sucursales, 'vendedores': vendedores, 'clientes': clientes})
        
        return redirect('clase:agregar_pedido')
    
    else:
        sucursales = Sucursal.objects.all()
        vendedores = Vendedor.objects.all()
        clientes = Cliente.objects.all()
        return render(request, 'core/agregar_pedido.html', {'sucursales': sucursales, 'vendedores': vendedores, 'clientes': clientes})
    
def about_me(request):
    return render(request, 'core/about_me.html')

@staff_member_required
def index_staff(request):
    return render(request, 'core/index_staff.html')

@login_required
def mis_datos(request):
    usuario = request.user
    try:
        perfil_usuario = UserProfile.objects.get(user=usuario)
    except UserProfile.DoesNotExist:
        perfil_usuario = None

    return render(request, 'core/mis_datos.html', {'perfil_usuario': perfil_usuario})

@login_required
def mis_datos_editar(request):
    usuario = request.user
    try:
        perfil_usuario = UserProfile.objects.get(user=usuario)
    except UserProfile.DoesNotExist:
        perfil_usuario = None

    if request.method == 'POST':
        if perfil_usuario:
            form = UserProfileForm(request.POST, request.FILES, instance=perfil_usuario)
        else:
            form = UserProfileForm(request.POST, request.FILES)
            
        if form.is_valid():
            perfil_usuario = form.save(commit=False)
            perfil_usuario.user = usuario
            if 'avatar-clear' in form.cleaned_data and perfil_usuario.avatar == 'default.jpg':
                pass
            elif 'avatar-clear' in form.cleaned_data:   
                perfil_usuario.avatar = None
            elif not request.FILES and not perfil_usuario.avatar:
                perfil_usuario.avatar = 'default.jpg'
            perfil_usuario.save()
            return redirect('clase:mis_datos')
    else:
        if perfil_usuario:
            form = UserProfileForm(instance=perfil_usuario)
        else:
            perfil_usuario = UserProfile(user=usuario, avatar='default.jpg')
            perfil_usuario.save()
            form = UserProfileForm(instance=perfil_usuario)

        if 'avatar-clear' in form.fields:
            del form.fields['avatar-clear']

    return render(request, 'core/mis_datos_editar.html', {'form': form})

