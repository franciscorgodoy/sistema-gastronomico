from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import EmpleadoForm
from .models import Empleado

# Create your views here.


@method_decorator(login_required, name="dispatch")
class ListEmpleado(generic.ListView):

    model = Empleado
    template_name = "empleados/inicio.html"
    paginate_by = 10

    def get_queryset(self):
        return Empleado.objects.filter(estado=True).order_by("apellido")


@method_decorator(login_required, name="dispatch")
class CreateEmpleado(generic.CreateView):

    model = Empleado
    form_class = EmpleadoForm
    template_name = "empleados/crear.html"
    success_url = "/empleados/?ok"


@method_decorator(login_required, name="dispatch")
class UpdateEmpleado(generic.UpdateView):

    model = Empleado
    form_class = EmpleadoForm
    template_name = "empleados/crear.html"
    success_url = "/empleados/?up"


@method_decorator(login_required, name="dispatch")
class DeleteEmpleado(generic.DeleteView):

    model = Empleado
    template_name = "empleados/delete_empleado.html"

    def post(self, request, *args, **kwars):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        return redirect("/empleados/?del")
