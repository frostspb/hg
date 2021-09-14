# Generated by Django 3.2.6 on 2021-09-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0008_auto_20210803_2000'),
        ('campaigns', '0027_alter_intentfeedssection_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='rejected',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='delivered',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='rejected',
        ),
        migrations.AddField(
            model_name='teams',
            name='rejected_percent',
            field=models.PositiveIntegerField(default=0, verbose_name='% of Leads Rejected'),
        ),
        migrations.AlterField(
            model_name='assetssection',
            name='titles',
            field=models.ManyToManyField(blank=True, related_name='jt_as', to='references.JobTitles'),
        ),
    ]