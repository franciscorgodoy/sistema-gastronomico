from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from sis_gastronomico.insumos.models import Insumo
from sis_gastronomico.stocks.forms import StockInsumoForm
from sis_gastronomico.stocks.models import StockInsumo


class InsumoForm(ModelForm):
    class Meta:
        model = Insumo
        fields = "__all__"

    def clean_nombre(self, *args, **kwargs):
        return self.cleaned_data.get("nombre").lower()

    def clean_descripcion(self, *args, **kwargs):
        return self.cleaned_data.get("descripcion").lower()


StockInsumoFormSet = inlineformset_factory(
    Insumo,
    StockInsumo,
    form=StockInsumoForm,
    can_delete=True,
    extra=1,
    fields="__all__",
)
