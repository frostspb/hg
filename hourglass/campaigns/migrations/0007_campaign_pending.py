# Generated by Django 3.0.5 on 2021-07-17 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_auto_20210716_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='pending',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Pending in Integration'),
        ),
    ]