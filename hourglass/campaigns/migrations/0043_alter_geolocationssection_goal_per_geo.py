# Generated by Django 3.2.6 on 2021-11-13 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0042_auto_20211111_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocationssection',
            name='goal_per_geo',
            field=models.FloatField(blank=True, null=True, verbose_name='Goal per Geo'),
        ),
    ]
