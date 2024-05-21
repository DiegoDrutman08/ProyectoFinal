from django.contrib import admin

from . import models

admin.site.site_title = "Sucursales"


class LocalidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    list_display_links = ("nombre",)


class SucursalAdmin(admin.ModelAdmin):
    list_display = (
        "localidad_id",
        "nombre",
        "telefono",
        "email",
        "descripcion",
        "fecha_actualizacion",
    )
    list_display_links = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("localidad_id", "nombre")
    list_filter = ("localidad_id",)
    date_hierarchy = "fecha_actualizacion"

admin.site.register(models.Localidad, LocalidadAdmin)
admin.site.register(models.Sucursal, SucursalAdmin)

admin.site.register(models.Cliente)
admin.site.register(models.Vendedor)
admin.site.register(models.Pedido)

