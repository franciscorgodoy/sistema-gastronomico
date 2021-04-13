from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView  # NOQA
from django.views.generic.list import ListView

from sis_gastronomico.compras.forms import (
    CompraForm,
    DetalleInsumoFormSet,
    DetalleProductoFormSet,
)
from sis_gastronomico.compras.models import Compra


# Create your views here.
@method_decorator(login_required, name="dispatch")
class ListCompras(ListView):
    model = Compra
    paginate_by = 10
    template_name = "compras/list_compras.html"

    def get_queryset(self, **kwargs):
        return Compra.objects.order_by("-fecha_modificacion")


@method_decorator(login_required, name="dispatch")
class CreateCompra(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = "compras/compra_form.html"
    success_url = "/compras/?ok"

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_insumo_form = DetalleInsumoFormSet()
        detalle_producto_form = DetalleProductoFormSet()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalle_insumo_form=detalle_insumo_form,
                detalle_producto_form=detalle_producto_form,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_insumo_form = DetalleInsumoFormSet(self.request.POST)
        detalle_producto_form = DetalleProductoFormSet(self.request.POST)
        if (
            form.is_valid()
            and detalle_insumo_form.is_valid()
            and detalle_producto_form.is_valid()
        ):
            return self.form_valid(form, detalle_insumo_form, detalle_producto_form)
        else:
            return self.form_invalid(form, detalle_insumo_form, detalle_producto_form)

    def form_valid(self, form, detalle_insumo_form, detalle_producto_form):
        self.object = form.save()
        detalle_insumo_form.instance = self.object
        detalle_insumo_form.save()
        detalle_producto_form.instance = self.object
        detalle_producto_form.save()

        gasto = self.object.gasto
        gasto.monto = self.object.precio_total
        gasto.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_insumo_form, detalle_producto_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalle_insumo_form=detalle_insumo_form,
                detalle_producto_form=detalle_producto_form,
            )
        )


@method_decorator(login_required, name="dispatch")
class DetailCompra(DetailView):
    model = Compra
    template_name = "compras/detail_compra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["precio_total_productos"] = sum(
            x.precio_total for x in self.object.detalleproducto_set.all()
        )
        context["precio_total_insumos"] = sum(
            x.precio_total for x in self.object.detalleinsumo_set.all()
        )

        return context


@method_decorator(login_required, name="dispatch")
class UpdateCompra(UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = "compras/compra_form.html"
    success_url = "/compras/?up"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        detalle_insumo_form = DetalleInsumoFormSet(instance=self.object)
        detalle_insumo_form.extra = 0
        detalle_producto_form = DetalleProductoFormSet(instance=self.object)
        detalle_producto_form.extra = 0

        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalle_insumo_form=detalle_insumo_form,
                detalle_producto_form=detalle_producto_form,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_insumo_form = DetalleInsumoFormSet(
            self.request.POST, instance=self.object
        )
        detalle_producto_form = DetalleProductoFormSet(
            self.request.POST, instance=self.object
        )
        if (
            form.is_valid()
            and detalle_insumo_form.is_valid()
            and detalle_producto_form.is_valid()
        ):
            return self.form_valid(form, detalle_insumo_form, detalle_producto_form)
        else:
            return self.form_invalid(form, detalle_insumo_form, detalle_producto_form)

    def form_valid(self, form, detalle_insumo_form, detalle_producto_form):
        self.object = form.save()
        detalle_insumo_form.instance = self.object
        detalle_insumo_form.save()
        detalle_producto_form.instance = self.object
        detalle_producto_form.save()

        gasto = self.object.gasto
        gasto.monto = self.object.precio_total
        gasto.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_insumo_form, detalle_producto_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalle_insumo_form=detalle_insumo_form,
                detalle_producto_form=detalle_producto_form,
            )
        )


@method_decorator(login_required, name="dispatch")
class DeleteCompra(DeleteView):
    model = Compra
    template_name = "compras/delete_compra.html"
    success_url = "/compras/?del"
