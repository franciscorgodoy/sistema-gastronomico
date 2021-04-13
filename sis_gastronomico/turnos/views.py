from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from sis_gastronomico.turnos.forms import HorarioForm, TurnoForm
from sis_gastronomico.turnos.models import Horario, Turno

# Create your views here.


@method_decorator(login_required, name="dispatch")
class CreateHorario(CreateView):

    model = Horario
    form_class = HorarioForm
    template_name = "turnos/horario_form.html"
    success_url = "/turnos/list_horario?ok"


@method_decorator(login_required, name="dispatch")
class CreateTurno(CreateView):

    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = "/turnos/?ok"


class DeleteTurno(DeleteView):

    model = Turno
    template_name = "turnos/delete_turno.html"
    success_url = "/turnos/?del"


class DeleteHorario(DeleteView):

    model = Horario
    template_name = "turnos/delete_horario.html"
    success_url = "/turnos/list_horario?del"


@method_decorator(login_required, name="dispatch")
class ListHorario(ListView):

    model = Horario
    paginate_by = 10
    template_name = "turnos/list_horario.html"

    def get_queryset(self):
        return Horario.objects.all().order_by("desde")


@method_decorator(login_required, name="dispatch")
class ListTurno(ListView):

    model = Turno
    paginate_by = 10
    template_name = "turnos/list_turno.html"

    def get_queryset(self):
        return Turno.objects.all().order_by("-fecha", "-fecha_creacion")


def no_active_turno(request):
    return render(request, "turnos/no_active_turno.html")


@method_decorator(login_required, name="dispatch")
class UpdateHorario(UpdateView):

    model = Horario
    form_class = HorarioForm
    template_name = "turnos/horario_form.html"
    success_url = "/turnos/list_horario?up"


@method_decorator(login_required, name="dispatch")
class UpdateTurno(UpdateView):

    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = "/turnos/?up"
