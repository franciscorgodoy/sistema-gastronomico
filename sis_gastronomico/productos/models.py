from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TipoProducto(models.Model):

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    tipo = models.CharField(unique=True, max_length=35)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "{:s}".format(self.tipo)


class Producto(models.Model):

    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=50)
    precio = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(99999.99)],
    )
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    tipo_producto = models.ForeignKey(
        TipoProducto, on_delete=models.CASCADE, verbose_name="Tipo Producto"
    )

    def __str__(self):
        return self.nombre
