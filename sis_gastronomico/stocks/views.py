from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from sis_gastronomico.insumos.models import Insumo
from sis_gastronomico.productos.models import Producto
from sis_gastronomico.stocks.forms import StockInsumoForm, StockProductoForm
from sis_gastronomico.stocks.models import StockInsumo, StockProducto

# Create your views here.


@method_decorator(login_required, name="dispatch")
class ListStockInsumo(generic.ListView):

    model = StockInsumo
    paginate_by = 10
    template_name = "stocks/list_stockInsumo.html"

    def get_queryset(self):
        return StockInsumo.objects.filter(insumo_id=self.kwargs.get("pk")).order_by(
            "-fecha_modificacion"
        )

    def get_context_data(self, **kwargs):
        context = super(ListStockInsumo, self).get_context_data(**kwargs)
        # insumo = Insumo.objects.filter(id=self.kwargs.get("pk"))
        insumo = Insumo.objects.get(id=self.kwargs.get("pk"))
        context["insumo"] = insumo
        context["stock_actual"] = StockInsumo.stockactual(insumo)
        return context


@method_decorator(login_required, name="dispatch")
class ListStockProducto(generic.ListView):

    model = StockProducto
    paginate_by = 10
    template_name = "stocks/list_stockProducto.html"

    def get_queryset(self):
        return StockProducto.objects.filter(producto_id=self.kwargs.get("pk")).order_by(
            "-fecha_modificacion"
        )

    def get_context_data(self, **kwargs):
        context = super(ListStockProducto, self).get_context_data(**kwargs)
        # producto = Producto.objects.filter(id=self.kwargs.get("pk"))
        producto = Producto.objects.get(id=self.kwargs.get("pk"))
        context["producto"] = producto
        context["stock_actual"] = StockProducto.stockactual(producto)
        return context


@method_decorator(login_required, name="dispatch")
class UpdateStockInsumo(generic.UpdateView):

    model = StockInsumo
    form_class = StockInsumoForm
    template_name = "stocks/create_stockInsumo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["insumo_ID"] = self.object.insumo.id
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.pk = None
        self.object.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "stocks:list_stockInsumo", kwargs={"pk": self.object.insumo.id}
            )
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name="dispatch")
class UpdateStockProducto(generic.UpdateView):

    model = StockProducto
    form_class = StockProductoForm
    template_name = "stocks/create_stockProducto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto_ID"] = self.object.producto.id
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.pk = None
        self.object.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "stocks:list_stockProducto", kwargs={"pk": self.object.producto.id}
            )
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
