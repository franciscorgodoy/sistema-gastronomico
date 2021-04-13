from django.urls import path

from sis_gastronomico.stocks.views import (
    ListStockInsumo,
    ListStockProducto,
    UpdateStockInsumo,
    UpdateStockProducto,
)

app_name = "stocks"
urlpatterns = [
    path(
        "list_stockInsumo/<int:pk>", ListStockInsumo.as_view(), name="list_stockInsumo"
    ),
    path(
        "list_stockProducto/<int:pk>",
        ListStockProducto.as_view(),
        name="list_stockProducto",
    ),
    path(
        "update_stockInsumo/<int:pk>",
        UpdateStockInsumo.as_view(),
        name="update_stockInsumo",
    ),
    path(
        "update_stockProducto/<int:pk>",
        UpdateStockProducto.as_view(),
        name="update_stockProducto",
    ),
]
