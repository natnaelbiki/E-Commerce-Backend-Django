# Generated by Django 4.0.4 on 2022-06-14 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='Zone',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='region',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('supplier', 'Supplier'), ('customer', 'Customer'), ('delivery', 'Delivery')], default='customer', max_length=20),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.DeleteModel(
            name='Zone',
        ),
    ]
