from django.contrib import admin

from sis_gastronomico.compras.models import Compra, DetalleInsumo, DetalleProducto


# Register your models here.
class DetalleInsumoInline(admin.TabularInline):
    model = DetalleInsumo
    # Mostramos dos inlines acíos por defecto
    extra = 1


class DetalleProductoInline(admin.TabularInline):
    model = DetalleProducto
    # Mostramos dos inlines acíos por defecto
    extra = 1


class CompraAdmin(admin.ModelAdmin):
    list_display = ("fecha", "precio_total")
    inlines = [DetalleInsumoInline, DetalleProductoInline]


admin.site.register(Compra, CompraAdmin)
admin.site.register(DetalleInsumo)
admin.site.register(DetalleProducto)
