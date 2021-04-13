from django.forms import ModelForm, TextInput
from django.forms.models import inlineformset_factory

from sis_gastronomico.productos.models import Producto, TipoProducto
from sis_gastronomico.stocks.forms import StockProductoForm
from sis_gastronomico.stocks.models import StockProducto


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        widgets = {"descripcion": TextInput(attrs={"class": "autocomplete"})}

    def clean_nombre(self, *args, **kwargs):
        return self.cleaned_data.get("nombre").lower()

    def clean_descripcion(self, *args, **kwargs):
        return self.cleaned_data.get("descripcion").lower()


class TipoProductoForm(ModelForm):
    class Meta:
        model = TipoProducto
        exclude = ["fecha_creacion", "fecha_modificacion"]

    def clean_tipo(self, *args, **kwargs):
        return self.cleaned_data.get("tipo").lower()

    def clean_descripcion(self, *args, **kwargs):
        return self.cleaned_data.get("descripcion").lower()


StockProductoFormSet = inlineformset_factory(
    Producto,
    StockProducto,
    form=StockProductoForm,
    can_delete=True,
    extra=1,
    fields="__all__",
)
