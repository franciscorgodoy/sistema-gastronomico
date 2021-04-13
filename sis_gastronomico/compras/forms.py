from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from sis_gastronomico.compras.models import Compra, DetalleInsumo, DetalleProducto
from sis_gastronomico.stocks.models import StockInsumo, StockProducto


class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = "__all__"
        exclude = ["gasto"]


class DetalleInsumoForm(ModelForm):
    class Meta:
        model = DetalleInsumo
        fields = "__all__"

    def clean(self):

        cantidad = 0
        if "cantidad" in self.cleaned_data:
            cantidad = self.cleaned_data["cantidad"]

            if self.get_stock_new_value() < 0:

                self.add_error(
                    "cantidad",
                    ValidationError(
                        "Cambiar la cantidad a %(new_cantidad)s provocaría que el stock quede en %(new_stock)s",
                        code="invalid",
                        params={
                            "new_cantidad": cantidad,
                            "new_stock": self.get_stock_new_value(),
                        },
                    ),
                )

    def get_stock_new_value(self):
        insumo = self.cleaned_data["insumo"]
        stock_actual = (
            StockInsumo.objects.filter(insumo=insumo)
            .order_by("fecha_modificacion")
            .last()
        )

        cantidad_stock_actual = stock_actual.cantidad
        cantidad_compra_nueva = self.cleaned_data["cantidad"]

        if self.initial:
            cantidad_compra_vieja = self.initial["cantidad"]
            cantidad_stock_nuevo = cantidad_stock_actual - (
                cantidad_compra_vieja - cantidad_compra_nueva
            )

        else:
            cantidad_compra_nueva = self.cleaned_data["cantidad"]
            cantidad_stock_nuevo = cantidad_stock_actual + cantidad_compra_nueva

        return cantidad_stock_nuevo


class DetalleProductoForm(ModelForm):
    class Meta:
        model = DetalleProducto
        fields = "__all__"

    def clean(self):

        cantidad = 0
        if "cantidad" in self.cleaned_data:
            cantidad = self.cleaned_data["cantidad"]
            if self.get_stock_new_value() < 0:

                self.add_error(
                    "cantidad",
                    ValidationError(
                        "Cambiar la cantidad a %(new_cantidad)s provocaría que el stock quede en %(new_stock)s",
                        code="invalid",
                        params={
                            "new_cantidad": cantidad,
                            "new_stock": self.get_stock_new_value(),
                        },
                    ),
                )

    def get_stock_new_value(self):
        producto = self.cleaned_data["producto"]
        stock_actual = (
            StockProducto.objects.filter(producto=producto)
            .order_by("fecha_modificacion")
            .last()
        )

        cantidad_stock_actual = stock_actual.cantidad
        cantidad_compra_nueva = self.cleaned_data["cantidad"]

        if self.initial:
            # En este caso es un UPDATE
            cantidad_compra_vieja = self.initial["cantidad"]
            cantidad_stock_nuevo = max(
                0,
                cantidad_stock_actual - (cantidad_compra_vieja - cantidad_compra_nueva),
            )

        else:
            cantidad_compra_nueva = self.cleaned_data["cantidad"]
            cantidad_stock_nuevo = cantidad_stock_actual + cantidad_compra_nueva

        return cantidad_stock_nuevo


class BaseInlineInsumoFormSet(BaseInlineFormSet):
    def save_new(self, form, commit):
        stock = StockInsumo()
        stock.insumo = form.cleaned_data["insumo"]
        stock.cantidad = form.get_stock_new_value()

        super().save_new(form, commit)
        stock.save()

    def save_existing(self, form, instance, commit):
        stock = StockInsumo()
        stock.insumo = form.cleaned_data["insumo"]
        stock.cantidad = form.get_stock_new_value()

        super().save_existing(form, instance, commit)
        stock.save()

    def clean(self):
        if any(self.errors):
            return
        insumos = []
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data["DELETE"]:
                    continue

                insumo = form.cleaned_data["insumo"]
                if insumo in insumos:
                    form.add_error(
                        "insumo", "No puede haber más de uno del mismo insumo"
                    )
                else:
                    insumos.append(insumo)


class BaseInlineProductoFormSet(BaseInlineFormSet):
    def save_new(self, form, commit):
        stock = StockProducto()
        stock.producto = form.cleaned_data["producto"]
        stock.cantidad = form.get_stock_new_value()

        super().save_new(form, commit)
        stock.save()

    def save_existing(self, form, instance, commit):
        stock = StockProducto()
        stock.producto = form.cleaned_data["producto"]
        stock.cantidad = form.get_stock_new_value()

        super().save_existing(form, instance, commit)
        stock.save()

    def clean(self):

        if any(self.errors):
            return
        productos = []
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data["DELETE"]:
                    continue

                producto = form.cleaned_data["producto"]
                if producto in productos:
                    form.add_error(
                        "producto", "No puede haber más de uno del mismo producto"
                    )
                else:
                    productos.append(producto)


DetalleInsumoFormSet = inlineformset_factory(
    Compra,
    DetalleInsumo,
    can_delete=True,
    extra=1,
    fields="__all__",
    formset=BaseInlineInsumoFormSet,
    form=DetalleInsumoForm,
)

DetalleProductoFormSet = inlineformset_factory(
    Compra,
    DetalleProducto,
    can_delete=True,
    extra=1,
    fields="__all__",
    formset=BaseInlineProductoFormSet,
    form=DetalleProductoForm,
)
