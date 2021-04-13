from django.core.validators import MinValueValidator
from django.db import models

from sis_gastronomico.insumos.models import Insumo
from sis_gastronomico.productos.models import Producto

# Create your models here.


class StockInsumo(models.Model):

    cantidad = models.SmallIntegerField(validators=[MinValueValidator(0)])
    insumo = models.ForeignKey(
        Insumo, on_delete=models.CASCADE, verbose_name="stock de insumo"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stock de Insumo"
        verbose_name_plural = "Stock de Insumos"
        db_table = "stock_Insumo"

    def __str__(self):
        return "{:d}".format(self.cantidad)

    @staticmethod
    def stockactual(insumo):
        return (
            StockInsumo.objects.filter(insumo=insumo)
            .order_by("fecha_modificacion")
            .last()
        )


class StockProducto(models.Model):

    cantidad = models.SmallIntegerField(validators=[MinValueValidator(0)])
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, verbose_name="stock de producto"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stock de Producto"
        verbose_name_plural = "Stock de Productos"
        db_table = "stock_Producto"

    def __str__(self):
        return "{:d}".format(self.cantidad)

    @staticmethod
    def stockactual(producto):
        return (
            StockProducto.objects.filter(producto=producto)
            .order_by("fecha_modificacion")
            .last()
        )
