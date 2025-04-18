# Generated by Django 5.1.7 on 2025-03-22 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InspectionTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(max_length=10, unique=True)),
                ('inspection_type', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('vehicle_make', models.CharField(max_length=100)),
                ('vin', models.CharField(max_length=100)),
                ('priority', models.CharField(choices=[('Critical', 'Critical'), ('Normal', 'Normal')], default='Normal', max_length=20)),
                ('tag', models.CharField(choices=[('Tag 1', 'Tag 1'), ('No Tag Assigned', 'No Tag Assigned')], default='No Tag Assigned', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Assigned', 'Assigned'), ('Completed', 'Completed')], default='Open', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('status', models.CharField(default='Available', max_length=20)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='InspectionSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection_date', models.DateField()),
                ('inspection_time', models.TimeField()),
                ('duration', models.IntegerField(default=1)),
                ('notes', models.TextField(blank=True)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inspection.inspectionticket')),
            ],
        ),
        migrations.AddField(
            model_name='inspectionticket',
            name='inspector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inspection.inspector'),
        ),
    ]
