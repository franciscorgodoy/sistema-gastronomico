# Generated by Django 3.0.8 on 2020-12-16 17:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0001_initial'),
        ('insumos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Producto', verbose_name='stock de producto')),
            ],
            options={
                'verbose_name': 'Stock de Producto',
                'verbose_name_plural': 'Stock de Productos',
                'db_table': 'stock_Producto',
            },
        ),
        migrations.CreateModel(
            name='StockInsumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumos.Insumo', verbose_name='stock de insumo')),
            ],
            options={
                'verbose_name': 'Stock de Insumo',
                'verbose_name_plural': 'Stock de Insumos',
                'db_table': 'stock_Insumo',
            },
        ),
    ]
