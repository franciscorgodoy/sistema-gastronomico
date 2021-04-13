from django.urls import path

from sis_gastronomico.gastos.views import (
    CreateAdelantoSueldo,
    CreateGasto,
    CreateTipoGasto,
    DeleteAdelantoSueldo,
    DeleteGasto,
    DeleteTipoGasto,
    ListAdelantoSueldo,
    ListGasto,
    ListTipoGasto,
    UpdateAdelantoSueldo,
    UpdateGasto,
    UpdateTipoGasto,
)

app_name = "gastos"
urlpatterns = [
    # path("", index, name="index"),
    path("", ListGasto.as_view(), name="index"),
    path("create_gasto", CreateGasto.as_view(), name="create_gasto"),
    path("create_tipo_gasto", CreateTipoGasto.as_view(), name="create_tipo_gasto"),
    path("delete_gasto/<int:pk>", DeleteGasto.as_view(), name="delete_gasto"),
    path(
        "delete_tipo_gasto/<int:pk>",
        DeleteTipoGasto.as_view(),
        name="delete_tipo_gasto",
    ),
    path("list_tipo_gasto", ListTipoGasto.as_view(), name="list_tipo_gasto"),
    path("update_gasto/<int:pk>", UpdateGasto.as_view(), name="update_gasto"),
    path(
        "update_tipo_gasto/<int:pk>",
        UpdateTipoGasto.as_view(),
        name="update_tipo_gasto",
    ),
    path(
        "create_adelantoSueldo",
        CreateAdelantoSueldo.as_view(),
        name="create_adelantoSueldo",
    ),
    path(
        "list_adelantoSueldo", ListAdelantoSueldo.as_view(), name="list_adelantoSueldo"
    ),
    path(
        "update_adelantoSueldo/<int:pk>",
        UpdateAdelantoSueldo.as_view(),
        name="update_adelantoSueldo",
    ),
    path(
        "delete_adelanto_sueldo/<int:pk>",
        DeleteAdelantoSueldo.as_view(),
        name="delete_adelanto_sueldo",
    ),
]
