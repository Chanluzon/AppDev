# Generated by Django 2.2.10 on 2024-05-21 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportticket',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='support.SupportTeam'),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='category',
            field=models.CharField(choices=[('Electrical', 'Electrical'), ('IT', 'IT'), ('Facilities', 'Facilities'), ('Other', 'Other')], default='Other', max_length=20),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=10),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], max_length=20),
        ),
        migrations.AlterField(
            model_name='supportticket',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]