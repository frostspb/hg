# Generated by Django 3.0.5 on 2021-07-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_campaign_nurturing_parameters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creativessection',
            name='subject_line',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Subject Line'),
        ),
    ]
