from django.urls import path

from sis_gastronomico.turnos.views import (
    CreateHorario,
    CreateTurno,
    DeleteHorario,
    DeleteTurno,
    ListHorario,
    ListTurno,
    UpdateHorario,
    UpdateTurno,
    no_active_turno,
)

app_name = "turnos"
urlpatterns = [
    path("", ListTurno.as_view(), name="index"),
    path("create_horario", CreateHorario.as_view(), name="create_horario"),
    path("create_turno", CreateTurno.as_view(), name="create_turno"),
    path("delete_turno/<int:pk>", DeleteTurno.as_view(), name="delete_turno",),
    path("delete_horario/<int:pk>", DeleteHorario.as_view(), name="delete_horario",),
    path("list_horario", ListHorario.as_view(), name="list_horario"),
    path("no_active_turno", no_active_turno, name="no_active_turno"),
    path("update_horario/<int:pk>", UpdateHorario.as_view(), name="update_horario"),
    path("update_turno/<int:pk>", UpdateTurno.as_view(), name="update_turno"),
]
