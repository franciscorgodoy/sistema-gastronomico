from django.urls import path  # NOQA

from sis_gastronomico.pedidos.views import (
    CreateMedioPago,
    CreateMedioPedido,
    CreatePedido,
    DeleteMedioPago,
    DeleteMedioPedido,
    DeletePedido,
    DetailPedido,
    ListMedioPago,
    ListMedioPedido,
    UpdateMedioPago,
    UpdateMedioPedido,
    UpdatePedido,
    informes,
    listPedido,
)

app_name = "pedidos"
urlpatterns = [
    # path("", index, name="index"),
    path("", listPedido, name="index"),
    path("list_medio_pago", ListMedioPago.as_view(), name="list_medio_pago"),
    path("list_medio_pedido", ListMedioPedido.as_view(), name="list_medio_pedido"),
    path(
        "create_medio_pedido", CreateMedioPedido.as_view(), name="create_medio_pedido"
    ),
    path("create_medio_pago", CreateMedioPago.as_view(), name="create_medio_pago"),
    path("", listPedido, name="index"),
    path("informes", informes, name="informes"),
    path("create_pedido", CreatePedido.as_view(), name="create_pedido"),
    path(
        "delete_medio_pago/<int:pk>",
        DeleteMedioPago.as_view(),
        name="delete_medio_pago",
    ),
    path(
        "delete_medio_pedido/<int:pk>",
        DeleteMedioPedido.as_view(),
        name="delete_medio_pedido",
    ),
    path("delete_pedido/<int:pk>", DeletePedido.as_view(), name="delete_pedido"),
    path("detail_pedido/<int:pk>", DetailPedido.as_view(), name="detail_pedido"),
    path(
        "update_medio_pago/<int:pk>",
        UpdateMedioPago.as_view(),
        name="update_medio_pago",
    ),
    path(
        "update_medio_pedido/<int:pk>",
        UpdateMedioPedido.as_view(),
        name="update_medio_pedido",
    ),
    path("update_pedido/<int:pk>", UpdatePedido.as_view(), name="update_pedido"),
]
