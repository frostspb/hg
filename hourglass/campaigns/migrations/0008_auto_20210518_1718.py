# Generated by Django 3.0.5 on 2021-05-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0003_auto_20210518_1718'),
        ('campaigns', '0007_campaign_tactics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targetsection',
            name='integration',
        ),
        migrations.RemoveField(
            model_name='targetsection',
            name='pacing',
        ),
        migrations.AddField(
            model_name='campaign',
            name='integration',
            field=models.CharField(choices=[('salesforce', 'Salesforce'), ('marketo', 'Marketo'), ('hub_spot', 'HubSpot'), ('integrate', 'Integrate'), ('lolagrove', 'Lolagrove')], default='salesforce', max_length=16),
        ),
        migrations.AddField(
            model_name='campaign',
            name='pacing',
            field=models.CharField(choices=[('even', 'Even'), ('front-load', 'Front-Load')], default='even', max_length=16),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='tactics',
            field=models.ManyToManyField(blank=True, null=True, to='references.Tactics'),
        ),
    ]
