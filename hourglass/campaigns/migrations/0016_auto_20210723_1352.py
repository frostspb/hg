# Generated by Django 3.0.5 on 2021-07-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0015_auto_20210723_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abmsection',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ABM'),
        ),
    ]
