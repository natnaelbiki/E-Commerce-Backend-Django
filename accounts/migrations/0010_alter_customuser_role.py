# Generated by Django 4.0.4 on 2022-05-31 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customuser_middle_name_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('supplier', 'Supplier'), ('admin', 'Admin'), ('customer', 'Customer'), ('delivery', 'Delivery')], default='Customer', max_length=20),
        ),
    ]
