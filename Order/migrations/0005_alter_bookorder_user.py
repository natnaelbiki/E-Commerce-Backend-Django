# Generated by Django 4.0.4 on 2022-05-28 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Order', '0004_alter_bookorder_status_alter_bookorder_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookorder',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
