from django.urls import path

from sis_gastronomico.compras.views import (
    CreateCompra,
    DeleteCompra,
    DetailCompra,
    ListCompras,
    UpdateCompra,
)

app_name = "compras"
urlpatterns = [
    path("", ListCompras.as_view(), name="index"),
    path("create_compra", CreateCompra.as_view(), name="create_compra"),
    path("detail_compra/<int:pk>", DetailCompra.as_view(), name="detail_compra"),
    path("update_compra/<int:pk>", UpdateCompra.as_view(), name="update_compra"),
    path("delete_compra/<int:pk>", DeleteCompra.as_view(), name="delete_compra"),
]
