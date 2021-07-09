# Generated by Django 3.0.5 on 2021-07-09 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0023_auto_20210701_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectionsettings',
            name='quality_per_row',
            field=models.IntegerField(blank=True, null=True, verbose_name='Change of Quality by Each Line'),
        ),
        migrations.AlterField(
            model_name='sectionsettings',
            name='quality_sector',
            field=models.IntegerField(blank=True, null=True, verbose_name='Change of Quality by Sector'),
        ),
    ]
