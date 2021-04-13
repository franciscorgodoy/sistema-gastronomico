from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from sis_gastronomico.gastos.forms import AdelantoSueldoForm, GastoForm, TipoGastoForm
from sis_gastronomico.gastos.models import AdelantoSueldo, Gasto, TipoGasto

# Create your views here.


@method_decorator(login_required, name="dispatch")
def index(request):

    gastos = Gasto.objects.all().order_by("-fecha_modificacion")[:10]
    for gasto in gastos:
        gasto.descripcion = gasto.descripcion.title()

    return render(request, "gastos/index.html", {"gastos": gastos})


@method_decorator(login_required, name="dispatch")
class CreateGasto(CreateView):

    model = Gasto
    form_class = GastoForm
    template_name = "gastos/gasto_form.html"
    success_url = "/gastos/?ok"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gastos = set()
        for gasto in Gasto.objects.values_list("descripcion", flat=True):
            gastos.add(gasto.title())
        context["gastos"] = gastos
        return context


@method_decorator(login_required, name="dispatch")
class CreateTipoGasto(CreateView):

    model = TipoGasto
    form_class = TipoGastoForm
    template_name = "gastos/tipo_gasto_form.html"
    success_url = "/gastos/list_tipo_gasto?tgok"


@method_decorator(login_required, name="dispatch")
class CreateAdelantoSueldo(CreateView):
    model = AdelantoSueldo
    form_class = AdelantoSueldoForm
    template_name = "gastos/adelantoSueldo_form.html"
    success_url = "/gastos/list_adelantoSueldo?ok"


@method_decorator(login_required, name="dispatch")
class DeleteGasto(DeleteView):

    model = Gasto
    template_name = "gastos/delete_gasto.html"
    success_url = "/gastos/?del"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class DeleteTipoGasto(DeleteView):

    model = TipoGasto
    template_name = "gastos/delete_tipo_gasto.html"
    success_url = "/gastos/list_tipo_gasto?tgdel"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class DeleteAdelantoSueldo(DeleteView):

    model = AdelantoSueldo
    template_name = "gastos/delete_adelanto_sueldo.html"
    success_url = "/gastos/list_adelantoSueldo?del"


@method_decorator(login_required, name="dispatch")
class ListGasto(ListView):

    model = Gasto
    paginate_by = 10
    template_name = "gastos/list_gasto.html"

    def get_queryset(self):
        return Gasto.objects.all().order_by("-fecha_modificacion")


@method_decorator(login_required, name="dispatch")
class ListTipoGasto(ListView):

    model = TipoGasto
    paginate_by = 10
    template_name = "gastos/list_tipo_gasto.html"

    def get_queryset(self):
        return TipoGasto.objects.all().order_by("tipo")


@method_decorator(login_required, name="dispatch")
class ListAdelantoSueldo(ListView):

    model = AdelantoSueldo
    paginate_by = 10
    template_name = "gastos/list_adelanto_sueldo.html"

    def get_queryset(self):
        return AdelantoSueldo.objects.all().order_by("-fecha_modificacion")


@method_decorator(login_required, name="dispatch")
class UpdateGasto(UpdateView):

    model = Gasto
    form_class = GastoForm
    template_name = "gastos/gasto_form.html"
    success_url = "/gastos/?up"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gastos = set()
        for gasto in Gasto.objects.values_list("descripcion", flat=True):
            gastos.add(gasto.title())
        context["gastos"] = gastos
        return context


@method_decorator(login_required, name="dispatch")
class UpdateTipoGasto(UpdateView):

    model = TipoGasto
    form_class = TipoGastoForm
    template_name = "gastos/tipo_gasto_form.html"
    success_url = "/gastos/list_tipo_gasto?tgup"


@method_decorator(login_required, name="dispatch")
class UpdateAdelantoSueldo(UpdateView):

    model = AdelantoSueldo
    form_class = AdelantoSueldoForm
    template_name = "gastos/adelantoSueldo_form.html"
    success_url = "/gastos/list_adelantoSueldo?up"
