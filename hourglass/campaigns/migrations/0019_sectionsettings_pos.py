# Generated by Django 3.0.5 on 2021-07-28 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0018_auto_20210728_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionsettings',
            name='pos',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]