# Generated by Django 2.2.10 on 2024-05-21 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TicketCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TicketPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tickets', to='support.SupportTeam')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.TicketCategory')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tickets', to=settings.AUTH_USER_MODEL)),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.TicketPriority')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.TicketStatus')),
            ],
        ),
        migrations.AddField(
            model_name='supportteam',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.TicketCategory'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='support.SupportTicket')),
            ],
        ),
    ]
