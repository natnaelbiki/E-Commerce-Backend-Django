# Generated by Django 4.0.4 on 2022-06-14 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0007_product_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=150, unique=True),
        ),
    ]
