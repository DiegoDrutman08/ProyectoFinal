from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Producto, Cliente, Vendedor, Pedido

def home(request):
    return render(request, "core/base.html")

def agregar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('producto')
        Producto.objects.create(nombre=nombre_producto)
        return redirect('core:home')
    else:
        return render(request, 'core/base.html')

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
