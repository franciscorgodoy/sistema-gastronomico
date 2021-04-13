from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Empleado(models.Model):
    nombre = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
    )
    apellido = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
    )
    dni = models.IntegerField(
        unique=True,
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(99999999, message="Ingrese un DNI valido"),
            MinValueValidator(11111111, message="Ingrese un DNI valido"),
        ],
    )
    fecha_nacimiento = models.DateField(null=False, blank=False)
    fecha_ingreso = models.DateField(
        null=False, blank=False, default=now
    )  # Fecha en la que el empleado ingreso a trabajar en la empresa
    estado = models.BooleanField(default=True)

    generos = models.TextChoices("Genero", "femenino masculino")
    genero = models.CharField(
        max_length=20, choices=generos.choices, default="femenino"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )  # Fecha en que se creo el empleado en el sistema
    fecha_modificacion = models.DateTimeField(
        auto_now=True
    )  # Fecha en que se modificp los datos del empleado en el sistema

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        db_table = "empleados"

    def __str__(self):
        return "{:s}, {:s}".format(self.apellido, self.nombre)
