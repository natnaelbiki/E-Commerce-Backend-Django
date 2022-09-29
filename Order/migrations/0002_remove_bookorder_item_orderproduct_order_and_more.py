# Generated by Django 4.0.4 on 2022-05-28 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookorder',
            name='item',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='Order.bookorder'),
        ),
        migrations.AlterField(
            model_name='bookorder',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=30),
        ),
    ]