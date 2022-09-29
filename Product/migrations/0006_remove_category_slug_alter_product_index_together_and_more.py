# Generated by Django 4.0.4 on 2022-05-29 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_alter_product_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'name')},
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]