# Generated by Django 3.0.8 on 2020-12-16 17:30

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(50)])),
                ('apellido', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(50)])),
                ('dni', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(99999999, message='Ingrese un DNI valido'), django.core.validators.MinValueValidator(11111111, message='Ingrese un DNI valido')])),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_ingreso', models.DateField(default=django.utils.timezone.now)),
                ('estado', models.BooleanField(default=True)),
                ('genero', models.CharField(choices=[('femenino', 'Femenino'), ('masculino', 'Masculino')], default='femenino', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'db_table': 'empleados',
            },
        ),
    ]
