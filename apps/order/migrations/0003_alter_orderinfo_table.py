# Generated by Django 3.2.1 on 2021-09-06 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='orderinfo',
            table='ag_order_info',
        ),
    ]
