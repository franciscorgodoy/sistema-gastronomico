# Generated by Django 3.0.8 on 2020-12-17 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0001_initial'),
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='proveedores.Proveedor'),
            preserve_default=False,
        ),
    ]
