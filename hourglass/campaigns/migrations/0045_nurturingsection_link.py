# Generated by Django 3.2.6 on 2021-12-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0044_alter_assetssection_titles'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurturingsection',
            name='link',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Creatives'),
        ),
    ]
