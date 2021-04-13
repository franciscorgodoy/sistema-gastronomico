from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from sis_gastronomico.pedidos.models import (
    DetallePedido,
    MedioPago,
    MedioPedido,
    Pedido,
)
from sis_gastronomico.stocks.models import StockProducto


class MedioPagoForm(ModelForm):
    class Meta:
        model = MedioPago
        fields = "__all__"


class MedioPedidoForm(ModelForm):
    class Meta:
        model = MedioPedido
        fields = "__all__"


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ["estado", "turno"]


class DetallePedidoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetallePedidoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

    def clean(self):
        cleaned_data = super().clean()

        if "cantidad" in cleaned_data and "producto" in cleaned_data:
            cantidad = cleaned_data["cantidad"]
            producto = cleaned_data["producto"]
            stock = StockProducto.stockactual(producto=producto)

            if (stock.cantidad - cantidad) < 0:
                self.add_error(
                    "cantidad",
                    ValidationError(
                        "El stock disponible es de %(cantidad_stock)s",
                        code="invalid",
                        params={"cantidad_stock": stock.cantidad},
                    ),
                )
        return cleaned_data

    class Meta:
        model = DetallePedido
        fields = "__all__"


class BaseInlineProductoFormSet(BaseInlineFormSet):
    def save_new(self, form, commit):
        # Crear nuevo stock en base al stock actual
        producto = form.cleaned_data["producto"]
        cantidad = form.cleaned_data["cantidad"]
        stock = StockProducto.stockactual(producto=producto)
        stock.pk = None
        stock.cantidad = stock.cantidad - cantidad
        stock.save()

        return super().save_new(form, commit=commit)

    def save_existing(self, form, instance, commit):
        if "producto" in form.changed_data:
            # Sumar a la la cantidad del registro de stock original
            stockoriginal = StockProducto.stockactual(producto=form.initial["producto"])
            stockoriginal.pk = None
            stockoriginal.cantidad = stockoriginal.cantidad + form.initial["cantidad"]
            stockoriginal.save()

            # Restar stock en el nuevo producto
            stocknuevo = StockProducto.stockactual(
                producto=form.cleaned_data["producto"]
            )
            stocknuevo.pk = None
            stocknuevo.cantidad = stocknuevo.cantidad - form.cleaned_data["cantidad"]
            stocknuevo.save()
        else:
            # Crear nuevo stock en base al stock actual
            stock = StockProducto.stockactual(producto=form.cleaned_data["producto"])
            stock.pk = None
            stock.cantidad = (
                stock.cantidad
                + form.initial["cantidad"]
                - form.cleaned_data["cantidad"]
            )
            stock.save()

        return super().save_existing(form, instance, commit=commit)

    def delete_existing(self, obj, commit):
        # Restar la cantidad del registro de stock
        stock = StockProducto.stockactual(producto=obj.producto)
        stock.pk = None
        stock.cantidad = stock.cantidad + obj.cantidad
        stock.save()

        return super().delete_existing(obj, commit=commit)

    def clean(self):

        if any(self.errors):
            return
        productos = dict()
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data["DELETE"]:
                    continue

                producto = form.cleaned_data["producto"]
                if producto in productos:
                    form.add_error(
                        "producto", "Este producto ya fue listado en el Pedido"
                    )
                else:
                    productos[producto] = 1


DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    DetallePedidoForm,
    can_delete=True,
    extra=1,
    formset=BaseInlineProductoFormSet,
)
