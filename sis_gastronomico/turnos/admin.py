from django.contrib import admin

from sis_gastronomico.turnos.models import Horario, Turno

# Register your models here.
admin.site.register(Horario)
admin.site.register(Turno)
