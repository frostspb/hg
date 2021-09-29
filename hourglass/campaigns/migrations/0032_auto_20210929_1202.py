# Generated by Django 3.2.6 on 2021-09-29 12:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0031_nurturingsection_nurturing_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='engagement_in_process',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='campaign',
            name='maximum_campaign_completeness',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]