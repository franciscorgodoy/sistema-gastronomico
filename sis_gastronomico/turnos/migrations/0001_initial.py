# Generated by Django 3.0.8 on 2020-12-16 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.CharField(max_length=35)),
                ('desde', models.TimeField()),
                ('hasta', models.TimeField()),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['desde'],
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('empleados', models.ManyToManyField(to='empleados.Empleado')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turnos.Horario')),
            ],
        ),
    ]
