from django.forms import ModelForm, TimeInput

from sis_gastronomico.turnos.models import Horario, Turno


class HorarioForm(ModelForm):
    class Meta:
        model = Horario
        fields = ["horario", "desde", "hasta"]
        widgets = {
            "desde": TimeInput(attrs={"class": "timepicker"}),
            "hasta": TimeInput(attrs={"class": "timepicker"}),
        }

    def clean_horario(self, *args, **kwargs):
        return self.cleaned_data.get("horario").lower()


class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ["horario", "empleados"]
