from django.contrib import admin

from sis_gastronomico.gastos.models import Gasto, TipoGasto

# Register your models here.

admin.site.register(Gasto)
admin.site.register(TipoGasto)
