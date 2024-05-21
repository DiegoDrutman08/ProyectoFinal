from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Localidad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=250, null=True, blank=True, verbose_name="descripción")

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        verbose_name = "localidad"
        verbose_name_plural = "localidades"

class Sucursal(models.Model):
    localidad = models.ForeignKey(
        Localidad, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="localidad"
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True, verbose_name="descripción")
    fecha_actualizacion = models.DateTimeField(
        null=True, blank=True, default=timezone.now, editable=False, verbose_name="fecha de actualización"
    )

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    codigo = models.PositiveIntegerField(unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_cliente')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_vendedor')
    fecha_actualizacion = models.DateField(
        null=True, blank=True, default=timezone.now, editable=False, verbose_name="fecha de actualización"
    )
 
    def __str__(self):
        return str(self.codigo)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/media/default.jpg'