# Generated by Django 3.0.5 on 2021-08-03 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0020_auto_20210803_1355'),
        ('references', '0007_company'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Company',
            new_name='CompanyRef',
        ),
    ]