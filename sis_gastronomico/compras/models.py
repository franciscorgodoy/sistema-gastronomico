from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from sis_gastronomico.gastos.models import Gasto, TipoGasto
from sis_gastronomico.insumos.models import Insumo
from sis_gastronomico.productos.models import Producto
from sis_gastronomico.proveedores.models import Proveedor


# Create your models here.
class Compra(models.Model):
    fecha = models.DateField(
        default=date.today, validators=[MaxValueValidator(date.today)]
    )
    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE, default=None)

    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    @property
    def precio_total(self):
        "Retorna la suma de los precios totales de todos los detalles de la compra"
        total = 0

        total += sum(d.precio_total for d in self.detalleinsumo_set.all())
        total += sum(d.precio_total for d in self.detalleproducto_set.all())

        return total

    def save(self, *args, **kwargs):

        if self._state.adding:
            tipo_gasto, _ = TipoGasto.objects.get_or_create(
                tipo="compra", defaults={"descripcion": "Descrpicion de la compra"}
            )

            self.gasto = Gasto.objects.create(
                descripcion="Compra de insumos/producto", monto=0, tipo_gasto=tipo_gasto
            )

        super(Compra, self).save(*args, **kwargs)


class DetalleInsumo(models.Model):
    precio_unitario = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(99999.99)],
    )
    cantidad = models.PositiveIntegerField()
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)

    @property
    def precio_total(self):
        return self.precio_unitario * self.cantidad


class DetalleProducto(models.Model):
    precio_unitario = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(99999.99)],
    )
    cantidad = models.PositiveIntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)

    @property
    def precio_total(self):
        return self.precio_unitario * self.cantidad
