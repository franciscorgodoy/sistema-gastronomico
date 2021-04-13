from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from sis_gastronomico.productos.forms import (
    ProductoForm,
    StockProductoFormSet,
    TipoProductoForm,
)
from sis_gastronomico.productos.models import Producto, TipoProducto

# Create your views here.


@method_decorator(login_required, name="dispatch")
def index(request):
    productos = Producto.objects.all().order_by("-fecha_modificacion")[:10]
    for producto in productos:
        producto.descripcion = producto.descripcion.title()

    return render(request, "productos/index.html", {"productos": productos})


@method_decorator(login_required, name="dispatch")
class ListarProductos(ListView):

    model = Producto
    paginate_by = 10
    template_name = "productos/listar_productos.html"

    def get_queryset(self):
        return Producto.objects.all().order_by("nombre")


@method_decorator(login_required, name="dispatch")
class ListarTipoProducto(ListView):

    model = TipoProducto
    paginate_by = 10
    template_name = "productos/listar_tipo_producto.html"

    def get_queryset(self):
        return TipoProducto.objects.all().order_by("-tipo")


@method_decorator(login_required, name="dispatch")
class CrearProducto(CreateView):

    model = Producto
    form_class = ProductoForm
    template_name = "productos/productos_form.html"
    success_url = "/productos/?ok"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = set()
        for producto in Producto.objects.values_list("nombre", flat=True):
            productos.add(producto.title())
        context["productos"] = productos
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        stock_producto_form = StockProductoFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, stock_producto_form=stock_producto_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        stock_producto_form = StockProductoFormSet(self.request.POST)
        if form.is_valid() and stock_producto_form.is_valid():
            return self.form_valid(form, stock_producto_form)
        else:
            return self.form_invalid(form, stock_producto_form)

    def form_valid(self, form, stock_producto_form):
        self.object = form.save()
        stock_producto_form.instance = self.object
        stock_producto_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, stock_producto_form):
        return self.render_to_response(
            self.get_context_data(form=form, stock_producto_form=stock_producto_form)
        )


@method_decorator(login_required, name="dispatch")
class CrearTipoProducto(CreateView):

    model = TipoProducto
    form_class = TipoProductoForm
    template_name = "productos/tipo_producto_form.html"
    success_url = "/productos/listar_tipo_producto?tgok"


@method_decorator(login_required, name="dispatch")
class BorrarProducto(DeleteView):

    model = Producto
    template_name = "productos/borrar_producto.html"
    success_url = "/productos/?del"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class BorrarTipoProducto(DeleteView):

    model = TipoProducto
    template_name = "productos/borrar_tipo_producto.html"
    success_url = "/productos/listar_tipo_producto?tgdel"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class UpdateProducto(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/productos_form.html"
    success_url = "/productos/?up"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = set()
        for producto in Producto.objects.values_list("descripcion", flat=True):
            productos.add(producto.title())
        context["productos"] = productos
        return context


@method_decorator(login_required, name="dispatch")
class UpdateTipoProducto(UpdateView):

    model = TipoProducto
    form_class = TipoProductoForm
    template_name = "productos/tipo_producto_form.html"
    success_url = "/productos/listar_tipo_producto?tgup"
