# Generated by Django 2.2.10 on 2024-05-21 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_auto_20240521_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportticket',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
