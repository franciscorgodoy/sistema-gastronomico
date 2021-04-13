from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save

from sis_gastronomico.empleados.models import Empleado

# Create your models here.


class TipoGasto(models.Model):

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    tipo = models.CharField(max_length=35)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "{:s}".format(self.tipo)


class AdelantoSueldo(models.Model):
    monto_pagado = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(99999.99)],
    )
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_pago = models.DateField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Adelanto de sueldo"
        verbose_name_plural = "Adelanto de sueldos"
        db_table = "Adelanto_Sueldo"

    def __str__(self):
        return "{:d}".format(self.monto_pagado)


class Gasto(models.Model):

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    descripcion = models.CharField(max_length=50)
    monto = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(99999.99)],
    )
    tipo_gasto = models.ForeignKey(
        TipoGasto, on_delete=models.CASCADE, verbose_name="Tipo Gasto"
    )
    adelanto = models.ForeignKey(
        AdelantoSueldo, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return "{:s}".format(self.descripcion)


def save_adelanto(sender, instance, **kwargs):
    if not kwargs["created"]:
        gasto = Gasto.objects.get(adelanto_id=instance.pk)
        gasto.monto = instance.monto_pagado
        gasto.save()
    else:
        gasto = Gasto()
        tipo_gasto, _ = TipoGasto.objects.get_or_create(
            tipo="adelanto de sueldo", defaults={"descripcion": "-"}
        )
        gasto.tipo_gasto = tipo_gasto
        gasto.monto = instance.monto_pagado
        gasto.adelanto = instance
        gasto.descripcion = "-"
        gasto.save()


post_save.connect(save_adelanto, sender=AdelantoSueldo)
