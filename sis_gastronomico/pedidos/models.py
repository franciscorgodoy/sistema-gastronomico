from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from sis_gastronomico.productos.models import Producto
from sis_gastronomico.turnos.models import Turno

# Create your models here.


class MedioPago(models.Model):
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    medio_pago = models.CharField(max_length=100)
    cuotas = models.IntegerField(validators=[MinValueValidator(0)])
    comision = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.medio_pago


class MedioPedido(models.Model):
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    medio_pedido = models.CharField(max_length=100)
    aumento = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.medio_pedido


def calc_num_pedido():
    pedidos_del_dia = Pedido.objects.filter(fecha=now().date()).order_by(
        "numero_pedido"
    )
    numero_pedido = 1
    if pedidos_del_dia:
        numero_pedido += pedidos_del_dia.first().numero_pedido
    return numero_pedido


class Pedido(models.Model):
    class EstadoPedido(models.IntegerChoices):
        NO_ENTREGADO = 0
        EN_CAMINO = 1
        ENTREGADO = 2
        CANCELADO = 3

    fecha = models.DateField(
        auto_now_add=True, validators=[MaxValueValidator(date.today)]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(
        choices=EstadoPedido.choices, default=EstadoPedido.NO_ENTREGADO
    )

    numero_pedido = models.SmallIntegerField(
        default=calc_num_pedido,
        blank=True,
        validators=[MaxValueValidator(9999), MinValueValidator(0)],
    )
    calle = models.CharField(max_length=100)
    altura = models.SmallIntegerField(
        validators=[MaxValueValidator(9999), MinValueValidator(0)]
    )
    piso = models.CharField(max_length=3, blank=True, null=True)
    departamento = models.CharField(max_length=3, blank=True, null=True)
    comentario = models.CharField(max_length=100, blank=True, null=True)
    medio_pago = models.ForeignKey(MedioPago, on_delete=models.CASCADE)
    medio_pedido = models.ForeignKey(MedioPedido, on_delete=models.CASCADE)
    precio_total = models.DecimalField(max_digits=7, decimal_places=2)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, default=0)


class DetallePedido(models.Model):

    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    cantidad = models.SmallIntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    @property
    def precio_total(self):
        return self.cantidad * self.producto.precio
