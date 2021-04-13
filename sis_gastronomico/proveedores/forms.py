from django.forms import ModelForm

# from django.forms.models import inlineformset_factory
from sis_gastronomico.proveedores.models import Proveedor


class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = "__all__"
        exclude = ["fecha_creacion", "fecha_modificacion"]

    def clean_nombre(self):
        return self.cleaned_data.get("nombre").lower()
