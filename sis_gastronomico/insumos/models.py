from django.db import models


# Create your models here.
class Insumo(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    fecha_modificacion = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.nombre
