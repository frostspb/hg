# Generated by Django 3.0.5 on 2021-06-04 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20210604_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='contact_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]