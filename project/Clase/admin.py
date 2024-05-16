from django.contrib import admin

from . import models

admin.site.site_title = "Productos"


class ProductoCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    list_display_links = ("nombre",)


class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "categoria_id",
        "nombre",
        "unidad_medida",
        "cantidad",
        "precio",
        "fecha_actualizacion",
    )
    list_display_links = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("categoria_id", "nombre")
    list_filter = ("categoria_id",)
    date_hierarchy = "fecha_actualizacion"

admin.site.register(models.ProductoCategoria, ProductoCategoriaAdmin)
admin.site.register(models.Producto, ProductoAdmin)

admin.site.register(models.Cliente)
admin.site.register(models.Vendedor)
admin.site.register(models.Pedido)

