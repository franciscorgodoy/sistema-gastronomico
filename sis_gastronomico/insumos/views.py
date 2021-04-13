from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from sis_gastronomico.insumos.forms import InsumoForm, StockInsumoFormSet
from sis_gastronomico.insumos.models import Insumo


def index(request):
    form = InsumoForm()
    return render(request, "insumos/home.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class ListInsumo(ListView):
    model = Insumo
    form_class = InsumoForm
    paginate_by = 10
    template_name = "insumos/list_insumo.html"

    def get_queryset(self, **kwargs):
        return Insumo.objects.order_by("nombre")


@method_decorator(login_required, name="dispatch")
class CreateInsumo(CreateView):

    model = Insumo
    form_class = InsumoForm
    template_name = "insumos/insumo_form.html"
    success_url = "/insumos/?ok"

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        stock_insumo_form = StockInsumoFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, stock_insumo_form=stock_insumo_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        stock_insumo_form = StockInsumoFormSet(self.request.POST)
        if form.is_valid() and stock_insumo_form.is_valid():
            return self.form_valid(form, stock_insumo_form)
        else:
            return self.form_invalid(form, stock_insumo_form)

    def form_valid(self, form, stock_insumo_form):
        self.object = form.save()
        stock_insumo_form.instance = self.object
        stock_insumo_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, stock_insumo_form):
        return self.render_to_response(
            self.get_context_data(form=form, stock_insumo_form=stock_insumo_form)
        )


@method_decorator(login_required, name="dispatch")
class DeleteInsumo(DeleteView):

    model = Insumo
    template_name = "insumos/delete_insumo.html"
    success_url = "/insumos/?del"


@method_decorator(login_required, name="dispatch")
class UpdateInsumo(UpdateView):

    model = Insumo
    form_class = InsumoForm
    template_name = "insumos/insumo_form.html"
    success_url = "/insumos/?up"
