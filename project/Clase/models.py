from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    codigo = models.PositiveIntegerField(unique=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_cliente')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_vendedor')    
 
    def __str__(self):
        return str(self.codigo)