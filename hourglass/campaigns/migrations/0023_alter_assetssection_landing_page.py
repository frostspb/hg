# Generated by Django 3.2.6 on 2021-08-19 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0022_auto_20210817_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetssection',
            name='landing_page',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Landing Page'),
        ),
    ]
