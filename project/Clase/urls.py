from django.urls import path
from . import views

app_name = "clase"

urlpatterns = [
    path("", views.home, name="home"),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('agregar_vendedor/', views.agregar_vendedor, name='agregar_vendedor'),
    path('agregar_pedido/', views.agregar_pedido, name='agregar_pedido'),
]
