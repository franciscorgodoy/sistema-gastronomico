from django.urls import path

from sis_gastronomico.proveedores.views import (
    BorrarProveedor,
    CrearProveedor,
    ListarProveedores,
    UpdateProveedor,
)

app_name = "proveedores"
urlpatterns = [
    path("", ListarProveedores.as_view(), name="index"),
    path("crear_proveedor/", CrearProveedor.as_view(), name="crear_proveedor"),
    path(
        "borrar_proveedor/<int:pk>", BorrarProveedor.as_view(), name="borrar_proveedor"
    ),
    path(
        "update_proveedor/<int:pk>", UpdateProveedor.as_view(), name="update_proveedor"
    ),
]
