from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from sis_gastronomico.proveedores.forms import ProveedorForm
from sis_gastronomico.proveedores.models import Proveedor


@method_decorator(login_required, name="dispatch")
def index(request):
    proveedores = Proveedor.objects.all().order_by("-fecha_modificacion")[:10]
    # for proveedor in proveedores:
    #     proveedor.descripcion = proveedor.descripcion.title()

    return render(request, "proveedores/index.html", {"proveedores": proveedores})


@method_decorator(login_required, name="dispatch")
class ListarProveedores(ListView):

    model = Proveedor
    paginate_by = 10
    template_name = "proveedores/listar_proveedores.html"

    def get_queryset(self):
        return Proveedor.objects.all().order_by("-fecha_modificacion")


@method_decorator(login_required, name="dispatch")
class CrearProveedor(CreateView):

    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/proveedores_form.html"
    success_url = "/proveedores/?ok"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proveedores = set()
        for proveedor in Proveedor.objects.values_list("nombre", flat=True):
            proveedores.add(proveedor.title())
        context["proveedores"] = proveedores
        return context


@method_decorator(login_required, name="dispatch")
class BorrarProveedor(DeleteView):

    model = Proveedor
    template_name = "proveedores/borrar_proveedor.html"
    success_url = "/proveedores/?del"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name="dispatch")
class UpdateProveedor(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/proveedores_form.html"
    success_url = "/proveedores/?up"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proveedores = set()
        # for proveedor in Proveedor.objects.values_list("descripcion", flat=True):
        #     proveedores.add(proveedor.title())
        context["proveedores"] = proveedores
        return context
