# Generated by Django 2.2.5 on 2022-01-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='order_id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='订单号'),
        ),
    ]
