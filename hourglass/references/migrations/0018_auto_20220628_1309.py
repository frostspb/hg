# Generated by Django 3.2.6 on 2022-06-28 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0017_auto_20220618_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leadtype',
            old_name='lead_type',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='seniority',
            old_name='seniority_title',
            new_name='name',
        ),
    ]