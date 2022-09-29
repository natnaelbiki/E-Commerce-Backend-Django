# Generated by Django 4.0.4 on 2022-06-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0010_alter_orderproduct_options_alter_orderproduct_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('ordered', 'Ordered')], default='pending', max_length=30),
        ),
    ]
