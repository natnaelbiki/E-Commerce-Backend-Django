# Generated by Django 4.0.4 on 2022-04-21 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(default='Piece', max_length=100),
        ),
    ]
