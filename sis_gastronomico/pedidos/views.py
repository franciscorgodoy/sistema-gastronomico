from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render  # NOQA
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime, now
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from sis_gastronomico.pedidos.forms import (
    DetallePedidoFormSet,
    MedioPagoForm,
    MedioPedidoForm,
    PedidoForm,
)
from sis_gastronomico.pedidos.models import MedioPago, MedioPedido, Pedido
from sis_gastronomico.turnos.models import Turno

# Create your views here.


@login_required
def informes(request):
    date = now().date()
    if "fecha" in request.GET:
        year, month, day = map(int, request.GET["fecha"].split("-"))
        date = datetime(year, month, day)
    turnos = Turno.objects.filter(fecha=date)
    context = {}
    context["turnos"] = []
    for turno in turnos:
        context["turnos"].append(
            {
                "turno": turno,
                # Pedidos por medio de pedido
                "medios_pedidos": Pedido.objects.filter(turno=turno)
                .values(tipo=F("medio_pedido__medio_pedido"))
                .annotate(cantidad=Count("medio_pedido__medio_pedido")),
                # Total de Pedidos
                "total_pedidos": Pedido.objects.filter(turno=turno).count(),
                # Total de productos por producto
                "total_tipos_productos": Pedido.objects.filter(turno=turno)
                .values(tipo=F("detallepedido__producto__nombre"))
                .annotate(cantidad=Sum("detallepedido__cantidad")),
                # Total de productos
                "total_productos": Pedido.objects.filter(turno=turno).aggregate(
                    total=Sum("detallepedido__cantidad")
                ),
                # Total de pedidos por medio de pago
                "total_medio_pago": Pedido.objects.filter(turno=turno)
                .values(tipo=F("medio_pago__medio_pago"))
                .annotate(total=Sum("precio_total")),
                "total_facturado": Pedido.objects.filter(turno=turno).aggregate(
                    total=Sum("precio_total")
                ),
            }
        )
    return render(request, "pedidos/informes.html", context)


@method_decorator(login_required, name="dispatch")
class CreatePedido(CreateView):

    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/pedido_form.html"
    success_url = "/pedidos/?ok"

    def get(self, request, *args, **kwargs):
        last_turno = Turno.objects.filter(fecha=now().date()).last()
        if last_turno is None or last_turno.activo is False:
            return HttpResponseRedirect(reverse("turnos:no_active_turno"))
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_pedido_form = DetallePedidoFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, detalle_pedido_form=detalle_pedido_form,)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_pedido_form = DetallePedidoFormSet(self.request.POST)
        if form.is_valid() and detalle_pedido_form.is_valid():
            return self.form_valid(form, detalle_pedido_form)
        else:
            return self.form_invalid(form, detalle_pedido_form)

    def form_valid(self, form, detalle_pedido_form):
        self.object = pedido = form.save(commit=False)
        pedidos = Pedido.objects.filter(fecha=now().date())
        if pedidos.count() == 0:
            pedido.numero_pedido = 1
        else:
            pedido.numero_pedido = pedidos.last().numero_pedido + 1
        pedido.turno = Turno.objects.last()
        pedido.save()
        detalle_pedido_form.instance = self.object
        detalles_pedido = detalle_pedido_form.save()
        total = sum([detalle_pedido.precio_total for detalle_pedido in detalles_pedido])
        pedido.precio_total = total
        pedido.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_pedido_form):
        return self.render_to_response(
            self.get_context_data(form=form, detalle_pedido_form=detalle_pedido_form,)
        )


@method_decorator(login_required, name="dispatch")
class CreateMedioPedido(CreateView):
    model = MedioPedido
    form_class = MedioPedidoForm
    template_name = "pedidos/medio_pedido_form.html"
    success_url = "/pedidos/list_medio_pedido?ok"


@method_decorator(login_required, name="dispatch")
class CreateMedioPago(CreateView):
    model = MedioPago
    form_class = MedioPagoForm
    template_name = "pedidos/medio_pago_form.html"
    success_url = "/pedidos/list_medio_pago?ok"


@method_decorator(login_required, name="dispatch")
class DetailPedido(DetailView):
    model = Pedido
    template_name = "pedidos/detail_pedido.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["precio_total"] = sum(
            dp.precio_total for dp in self.object.detallepedido_set.all()
        )
        return context


@method_decorator(login_required, name="dispatch")
class DeletePedido(DeleteView):
    model = Pedido
    template_name = "pedidos/delete_pedido.html"
    success_url = "/pedidos/?del"


@method_decorator(login_required, name="dispatch")
class DeleteMedioPedido(DeleteView):

    model = MedioPedido
    template_name = "pedidos/delete_medio_pedido.html"
    success_url = "/pedidos/list_medio_pedido?del"


@method_decorator(login_required, name="dispatch")
class DeleteMedioPago(DeleteView):

    model = MedioPago
    template_name = "pedidos/delete_medio_pago.html"
    success_url = "/pedidos/list_medio_pago?del"


@login_required
def listPedido(request):

    if request.POST.get("encamino"):
        pedido_id = request.POST.get("pedido_id")
        print(pedido_id)
        pedido = Pedido.objects.get(pk=pedido_id)
        pedido.estado = Pedido.EstadoPedido.EN_CAMINO
        pedido.save()
    elif request.POST.get("entregado"):
        pedido_id = request.POST.get("pedido_id")
        pedido = Pedido.objects.get(pk=pedido_id)
        pedido.estado = Pedido.EstadoPedido.ENTREGADO
        pedido.save()

    context = {}
    date = now().date()
    if "fecha" in request.GET:
        year, month, day = map(int, request.GET["fecha"].split("-"))
        date = datetime(year, month, day)
    context["pnentregados"] = (
        Pedido.objects.filter(fecha=date, estado=0)
        .order_by("fecha_creacion")
        .prefetch_related(
            "detallepedido_set",
            "detallepedido_set__producto",
            "detallepedido_set__producto",
            "medio_pedido",
            "medio_pago",
        )
    )
    context["pencamino"] = (
        Pedido.objects.filter(fecha=date, estado=1)
        .order_by("-fecha_creacion")
        .prefetch_related(
            "detallepedido_set",
            "detallepedido_set__producto",
            "detallepedido_set__producto",
            "medio_pedido",
            "medio_pago",
        )
    )
    context["pentregados"] = (
        Pedido.objects.filter(fecha=date, estado=2)
        .order_by("-fecha_creacion")
        .prefetch_related(
            "detallepedido_set",
            "detallepedido_set__producto",
            "detallepedido_set__producto",
            "medio_pedido",
            "medio_pago",
        )
    )
    return render(request, "pedidos/list_pedido.html", context)


@method_decorator(login_required, name="dispatch")
class ListMedioPedido(ListView):
    model = MedioPedido
    paginate_by = 10
    template_name = "pedidos/list_medio_pedido.html"

    def get_queryset(self, **kwargs):
        return MedioPedido.objects.order_by("medio_pedido")


@method_decorator(login_required, name="dispatch")
class ListMedioPago(ListView):
    model = MedioPago
    paginate_by = 10
    template_name = "pedidos/list_medio_pago.html"

    def get_queryset(self, **kwargs):
        return MedioPago.objects.order_by("medio_pago")


@method_decorator(login_required, name="dispatch")
class UpdatePedido(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/pedido_form.html"
    success_url = "/pedidos/?up"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        detalle_pedido_form = DetallePedidoFormSet(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form, detalle_pedido_form=detalle_pedido_form,)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_pedido_form = DetallePedidoFormSet(
            self.request.POST, instance=self.object
        )
        if form.is_valid() and detalle_pedido_form.is_valid():
            return self.form_valid(form, detalle_pedido_form)
        else:
            return self.form_invalid(form, detalle_pedido_form)

    def form_valid(self, form, detalle_pedido_form):
        self.object = form.save()
        detalle_pedido_form.instance = self.object
        detalle_pedido_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalle_pedido_form):
        return self.render_to_response(
            self.get_context_data(form=form, detalle_pedido_form=detalle_pedido_form,)
        )


@method_decorator(login_required, name="dispatch")
class UpdateMedioPedido(UpdateView):

    model = MedioPedido
    form_class = MedioPedidoForm
    template_name = "pedidos/medio_pedido_form.html"
    success_url = "/pedidos/list_medio_pedido?up"


@method_decorator(login_required, name="dispatch")
class UpdateMedioPago(UpdateView):

    model = MedioPago
    form_class = MedioPagoForm
    template_name = "pedidos/medio_pago_form.html"
    success_url = "/pedidos/list_medio_pago?up"
