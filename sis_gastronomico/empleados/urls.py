from django.urls import path

from . import views

app_name = "empleados"
urlpatterns = [
    path("", views.ListEmpleado.as_view(), name="inicio"),
    path("create_empleado/", views.CreateEmpleado.as_view(), name="create_empleado"),
    path(
        "update_empleado/<int:pk>/",
        views.UpdateEmpleado.as_view(),
        name="update_empleado",
    ),
    path(
        "delete_empleado/<int:pk>/",
        views.DeleteEmpleado.as_view(),
        name="delete_empleado",
    ),
]
