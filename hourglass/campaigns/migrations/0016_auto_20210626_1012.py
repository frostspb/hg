# Generated by Django 3.0.5 on 2021-06-26 10:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0015_jobtitlessection_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intentfeedssection',
            name='generated',
        ),
        migrations.AddField(
            model_name='campaign',
            name='intent_feed_goal_percent',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='campaign',
            name='intent_feed_lead_generated',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='intentfeedssection',
            name='companies_count',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Companies Generated'),
        ),
    ]
