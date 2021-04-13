from django.db import models

from sis_gastronomico.empleados.models import Empleado

# Create your models here.


class Horario(models.Model):

    horario = models.CharField(max_length=35)
    desde = models.TimeField()
    hasta = models.TimeField()
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["desde"]

    def __str__(self):
        return "{:s} - De {:s} a {:s}".format(
            self.horario.title(),
            self.desde.strftime("%H:%M"),
            self.hasta.strftime("%H:%M"),
        )


class Turno(models.Model):

    horario = models.ForeignKey(Horario, models.CASCADE)
    fecha = models.DateField(auto_now=True)
    empleados = models.ManyToManyField(Empleado)
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return "{:s} - {:s} ".format(str(self.fecha), str(self.horario))
