from django.forms import ModelForm, TextInput

# from django.forms.models import inlineformset_factory
from sis_gastronomico.gastos.models import AdelantoSueldo, Gasto, TipoGasto


class GastoForm(ModelForm):
    class Meta:
        model = Gasto
        exclude = ["fecha_creacion", "fecha_modificacion"]
        widgets = {"descripcion": TextInput(attrs={"class": "autocomplete"})}

    def clean_descripcion(self, *args, **kwargs):
        return self.cleaned_data.get("descripcion").lower()


class TipoGastoForm(ModelForm):
    class Meta:
        model = TipoGasto
        exclude = ["fecha_creacion", "fecha_modificacion"]

    def clean_tipo(self, *args, **kwargs):
        return self.cleaned_data.get("tipo").lower()

    def clean_descripcion(self, *args, **kwargs):
        return self.cleaned_data.get("descripcion").lower()


class AdelantoSueldoForm(ModelForm):
    class Meta:
        model = AdelantoSueldo
        fields = "__all__"
        exclude = ["fecha_pago", "fecha_modificacion"]
