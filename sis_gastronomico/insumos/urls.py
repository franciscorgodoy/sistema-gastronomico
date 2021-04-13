from django.urls import path

from sis_gastronomico.insumos.views import (
    CreateInsumo,
    DeleteInsumo,
    ListInsumo,
    UpdateInsumo,
)

app_name = "insumos"
urlpatterns = [
    path("", ListInsumo.as_view(), name="index"),
    path("create_insumo", CreateInsumo.as_view(), name="create_insumo"),
    path("delete_insumo/<int:pk>", DeleteInsumo.as_view(), name="delete_insumo"),
    path("update_insumo/<int:pk>", UpdateInsumo.as_view(), name="update_insumo"),
]
