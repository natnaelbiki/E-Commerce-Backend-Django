# Generated by Django 4.0.4 on 2022-05-28 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Order', '0003_alter_bookorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookorder',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='bookorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]