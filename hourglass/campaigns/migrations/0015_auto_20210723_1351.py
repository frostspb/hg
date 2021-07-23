# Generated by Django 3.0.5 on 2021-07-23 13:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0014_auto_20210720_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teams',
            options={'verbose_name': 'Teams', 'verbose_name_plural': 'Teams'},
        ),
        migrations.AddField(
            model_name='abmsection',
            name='name',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abmsection',
            name='percent',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
