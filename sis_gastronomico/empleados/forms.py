from django.forms import ModelForm

# from django.forms.models import inlineformset_factory
from sis_gastronomico.empleados.models import Empleado


class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = "__all__"
        exclude = ["estado", "fecha_creacion", "fecha_modificacion"]

    def clean_nombre(self):
        return self.cleaned_data.get("nombre").lower()

    def clean_apellido(self):
        return self.cleaned_data.get("apellido").lower()
