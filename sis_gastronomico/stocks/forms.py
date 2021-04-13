from django.forms import HiddenInput, ModelForm

from sis_gastronomico.stocks.models import StockInsumo, StockProducto


class StockInsumoForm(ModelForm):
    class Meta:
        model = StockInsumo
        fields = "__all__"
        exclude = ("fecha_creacion", "fecha_modificacion")
        widgets = {"insumo": HiddenInput}

    def __init__(self, *args, **kwargs):
        super(StockInsumoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False


class StockProductoForm(ModelForm):
    class Meta:
        model = StockProducto
        fields = "__all__"
        exclude = ("fecha_creacion", "fecha_modificacion")
        widgets = {"producto": HiddenInput}

    def __init__(self, *args, **kwargs):
        super(StockProductoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
