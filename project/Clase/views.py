from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Producto, Cliente, Vendedor, Pedido
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import forms, models
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

def home(request):
    return render(request, "clase/index.html")

class ProductoCategoriaList(ListView):
    model = models.ProductoCategoria

    def get_queryset(self) -> QuerySet:
        if self.request.GET.get("consulta"):
            consulta = self.request.GET.get("consulta")
            object_list = models.ProductoCategoria.objects.filter(nombre__icontains=consulta)
        else:
            object_list = models.ProductoCategoria.objects.all()
        return object_list

class ProductoCategoriaCreate(CreateView):
    model = models.ProductoCategoria
    form_class = forms.ProductoCategoriaForm
    success_url = reverse_lazy("clase:home")

class ProductoCategoriaUpdate(UpdateView):
    model = models.ProductoCategoria
    form_class = forms.ProductoCategoriaForm
    success_url = reverse_lazy("clase:productocategoria_list")

class ProductoCategoriaDetail(DetailView):
    model = models.ProductoCategoria

class ProductoCategoriaDelete(DeleteView):
    model = models.ProductoCategoria
    success_url = reverse_lazy("clase:productocategoria_list")

class ProductoList(ListView):
    model = models.Producto

    def get_queryset(self) -> QuerySet:
        if self.request.GET.get("consulta"):
            consulta = self.request.GET.get("consulta")
            object_list = models.Producto.objects.filter(nombre__icontains=consulta)
        else:
            object_list = models.Producto.objects.all()
        return object_list


class ProductoCreate(CreateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("clase:home")


class ProductoUpdate(UpdateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("clase:producto_list")


class ProductoDetail(DetailView):
    model = models.Producto


class ProductoDelete(DeleteView):
    model = models.Producto
    success_url = reverse_lazy("clase:producto_list")


def agregar_cliente(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('cliente')
        Cliente.objects.create(nombre=nombre_cliente)
        return redirect('core:home')
    else:
        return render(request, 'core/base.html')

def agregar_vendedor(request):
    if request.method == 'POST':
        nombre_vendedor = request.POST.get('vendedor')
        edad_vendedor = request.POST.get('edad')
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
        producto_id = request.POST.get('productos')
        vendedor_id = request.POST.get('vendedores')
        cliente_id = request.POST.get('clientes')
        
        try:
            producto = Producto.objects.get(id=producto_id)
            vendedor = Vendedor.objects.get(id=vendedor_id)
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Verificar si el código ya existe en la base de datos
            while True:
                try:
                    pedido = Pedido.objects.create(codigo=codigo, producto=producto, vendedor=vendedor, cliente=cliente)
                    break
                except IntegrityError:
                    # Generar un nuevo código si el actual ya existe
                    codigo += "_1"  # Puedes modificar esto según tu lógica de generación de códigos
        except (Producto.DoesNotExist, Vendedor.DoesNotExist, Cliente.DoesNotExist):
            error_message = "Uno o más objetos no existen"
            productos = Producto.objects.all()
            vendedores = Vendedor.objects.all()
            clientes = Cliente.objects.all()
            return render(request, 'core/agregar_pedido.html', {'error_message': error_message, 'productos': productos, 'vendedores': vendedores, 'clientes': clientes})
        
        return redirect('core:home')
    
    else:
        productos = Producto.objects.all()
        vendedores = Vendedor.objects.all()
        clientes = Cliente.objects.all()
        return render(request, 'core/agregar_pedido.html', {'productos': productos, 'vendedores': vendedores, 'clientes': clientes})
