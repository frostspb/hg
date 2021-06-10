# Generated by Django 3.0.5 on 2021-06-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0007_auto_20210610_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetssection',
            name='percent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='companysizesection',
            name='percent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='geolocationssection',
            name='percent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='industriessection',
            name='percent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='intentfeedssection',
            name='percent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='jobtitlessection',
            name='percent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='revenuesection',
            name='percent',
            field=models.FloatField(default=0),
        ),
    ]
