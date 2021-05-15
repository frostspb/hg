# Generated by Django 3.0.5 on 2021-05-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_auto_20210508_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='bottom_percent',
            field=models.FloatField(default=0, verbose_name='Bottom Leads Percent'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='middle_percent',
            field=models.FloatField(default=0, verbose_name='Middle Leads Percent'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_percent',
            field=models.FloatField(default=0, verbose_name='Top Leads Percent'),
        ),
        migrations.AlterField(
            model_name='assetssection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companysizesection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customquestionssection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='geolocationssection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='industriessection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='intentfeedssection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobtitlessection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='revenuesection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='targetsection',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]