# Generated by Django 3.0.5 on 2021-07-14 17:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='ta_volume',
            field=models.PositiveIntegerField(default=0, verbose_name='Target Audience Volume (in cubes)'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='dashboard_string_count',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], verbose_name='Lead Goal Lower Lines (Dashboard View)'),
        ),
    ]
