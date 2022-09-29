# Generated by Django 4.0.4 on 2022-06-14 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0013_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=30),
        ),
    ]
