# Generated by Django 4.0.4 on 2022-05-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_alter_bookorder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bookorder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('ordered', 'Ordered'), ('delivered', 'Delivered')], default='pending', max_length=30),
        ),
    ]