from django.urls import path

from sis_gastronomico.productos.views import (
    BorrarProducto,
    BorrarTipoProducto,
    CrearProducto,
    CrearTipoProducto,
    ListarProductos,
    ListarTipoProducto,
    UpdateProducto,
    UpdateTipoProducto,
)

app_name = "productos"
urlpatterns = [
    # path("", index, name="index"),
    path("", ListarProductos.as_view(), name="index"),
    path("crear_producto/", CrearProducto.as_view(), name="crear_producto"),
    path(
        "crear_tipo_producto", CrearTipoProducto.as_view(), name="crear_tipo_producto"
    ),
    path("borrar_producto/<int:pk>", BorrarProducto.as_view(), name="borrar_producto"),
    path(
        "borrar_tipo_producto/<int:pk>",
        BorrarTipoProducto.as_view(),
        name="borrar_tipo_producto",
    ),
    path(
        "listar_tipo_producto",
        ListarTipoProducto.as_view(),
        name="listar_tipo_producto",
    ),
    path("update_producto/<int:pk>", UpdateProducto.as_view(), name="update_producto"),
    path(
        "update_tipo_producto/<int:pk>",
        UpdateTipoProducto.as_view(),
        name="update_tipo_producto",
    ),
]
