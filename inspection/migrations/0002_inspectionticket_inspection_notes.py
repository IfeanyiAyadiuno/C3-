# Generated by Django 5.2 on 2025-04-09 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectionticket',
            name='inspection_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
