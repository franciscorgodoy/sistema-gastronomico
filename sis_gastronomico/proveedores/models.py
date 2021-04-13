from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models


# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=75,
        null=False,
        blank=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(75)],
    )

    direccion = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
    )

    telefono = models.BigIntegerField(
        unique=True,
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(9999999999, message="Ingrese un telefono valido"),
            MinValueValidator(111111111, message="Ingrese un telefono valido"),
        ],
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedores"

    def __str__(self):
        return "{:s}, {:s}".format(self.nombre, self.direccion)
