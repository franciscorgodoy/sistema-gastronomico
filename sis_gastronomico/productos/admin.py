from django.contrib import admin

from sis_gastronomico.productos.models import Producto, TipoProducto

# Register your models here.

admin.site.register(Producto)
admin.site.register(TipoProducto)
