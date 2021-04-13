import json

from django.conf import settings


def settings_context(_request):
    return {"settings": settings}


def get_version(request):
    with open("./version.json") as f:
        data = json.load(f)
    version = data["version"]
    fecha = data["fecha"]

    return {"version": version, "fecha": fecha}
