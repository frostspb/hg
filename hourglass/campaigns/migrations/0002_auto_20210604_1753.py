# Generated by Django 3.0.5 on 2021-06-04 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='contact_name',
            new_name='managed_by',
        ),
    ]
