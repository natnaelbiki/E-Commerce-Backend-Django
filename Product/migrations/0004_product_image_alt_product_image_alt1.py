# Generated by Django 4.0.4 on 2022-05-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_product_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_alt',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_alt1',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d'),
        ),
    ]