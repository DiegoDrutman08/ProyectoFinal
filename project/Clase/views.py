from .models import Producto, Cliente, Vendedor, Pedido
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
        nombre_cliente = request.POST.get('nombre')
        direccion_cliente = request.POST.get('direccion')
        email_cliente = request.POST.get('email')
        edad_cliente = request.POST.get('edad')

        # Verificar si ya existe un cliente con el mismo nombre
        if Cliente.objects.filter(nombre=nombre_cliente).exists():
            messages.error(request, 'Ya existe un cliente con este nombre')
            return render(request, 'core/index.html', {'mensaje': 'Ya existe un cliente con este nombre'})

        # Si no existe, crear el cliente
        Cliente.objects.create(nombre=nombre_cliente, direccion=direccion_cliente, email=email_cliente, edad=edad_cliente)

        return redirect('clase:agregar_pedido')
    else:
        return render(request, 'core/base.html')
    
def agregar_vendedor(request):
    if request.method == 'POST':
        nombre_vendedor = request.POST.get('vendedor')
        edad_vendedor = request.POST.get('edad')

        # Verificar si ya existe un vendedor con el mismo nombre
        if Vendedor.objects.filter(nombre=nombre_vendedor).exists():
            messages.error(request, 'Ya existe un vendedor con este nombre')
            return render(request, 'core/index_staff.html', {'mensaje': 'Ya existe un vendedor con este nombre'})
        
        # Si no existe, crear el vendedor
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
            
            # Verificar si ya existe un pedido con el mismo código
            while Pedido.objects.filter(codigo=codigo).exists():
                messages.error(request, 'Ya existe un pedido con este codigo')
                return render(request, 'core/agregar_pedido.html', {'mensaje': 'Ya existe un pedido con este codigo'})
            
            pedido = Pedido.objects.create(codigo=codigo, producto=producto, vendedor=vendedor, cliente=cliente)
        except (Producto.DoesNotExist, Vendedor.DoesNotExist, Cliente.DoesNotExist):
            error_message = "Uno o más objetos no existen"
            productos = Producto.objects.all()
            vendedores = Vendedor.objects.all()
            clientes = Cliente.objects.all()
            return render(request, 'core/agregar_pedido.html', {'error_message': error_message, 'productos': productos, 'vendedores': vendedores, 'clientes': clientes})
        except IntegrityError:
            error_message = "Ya existe un pedido con este código"
            productos = Producto.objects.all()
            vendedores = Vendedor.objects.all()
            clientes = Cliente.objects.all()
            return render(request, 'core/agregar_pedido.html', {'error_message': error_message, 'productos': productos, 'vendedores': vendedores, 'clientes': clientes})
        
        return redirect('clase:agregar_pedido')
    
    else:
        productos = Producto.objects.all()
        vendedores = Vendedor.objects.all()
        clientes = Cliente.objects.all()
        return render(request, 'core/agregar_pedido.html', {'productos': productos, 'vendedores': vendedores, 'clientes': clientes})
    
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

