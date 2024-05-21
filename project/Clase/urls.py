from django.urls import path

from . import views

app_name = "clase"

urlpatterns = [
    path("", views.home, name="home"),
    path("localidad/create/", views.LocalidadCreate.as_view(), name="localidad_create"),
    path("localidad/list/", views.LocalidadList.as_view(), name="localidad_list"),
    path("localidad/detail/<int:pk>", views.LocalidadDetail.as_view(), name="localidad_detail"),
    path("localidad/update/<int:pk>", views.LocalidadUpdate.as_view(), name="localidad_update"),
    path("localidad/delete/<int:pk>", views.LocalidadDelete.as_view(), name="localidad_delete"),
    path('index_staff/', views.index_staff, name='index_staff'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('agregar_vendedor/', views.agregar_vendedor, name='agregar_vendedor'),
    path('agregar_pedido/', views.agregar_pedido, name='agregar_pedido'),
    path('about_me/', views.about_me, name='about_me'),
    path('mis_datos/', views.mis_datos, name='mis_datos'),
    path('mis-datos/editar/', views.mis_datos_editar, name='mis_datos_editar'),
]

urlpatterns += [
    path("clase/list/", views.SucursalList.as_view(), name="sucursal_list"),
    path("clase/create/", views.SucursalCreate.as_view(), name="sucursal_create"),
    path("clase/detail/<int:pk>", views.SucursalDetail.as_view(), name="sucursal_detail"),
    path("clase/update/<int:pk>", views.SucursalUpdate.as_view(), name="sucursal_update"),
    path("clase/delete/<int:pk>", views.SucursalDelete.as_view(), name="sucursal_delete"),
]
