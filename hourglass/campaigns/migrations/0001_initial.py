# Generated by Django 3.0.5 on 2021-04-28 18:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_fsm
import hourglass.campaigns.models
import model_clone.mixins.clone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('references', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('customer_information', models.CharField(max_length=250, verbose_name='Customer information')),
                ('contact_name', models.CharField(max_length=250, verbose_name='Contact Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('name', models.CharField(max_length=250, verbose_name='Campaign Name')),
                ('active', models.BooleanField(default=True)),
                ('start_offset', models.PositiveSmallIntegerField(verbose_name='Start Date offset in days')),
                ('end_offset', models.PositiveSmallIntegerField(verbose_name='End Date offset in days')),
                ('audience_targeted', models.IntegerField(verbose_name='Audience Targeted')),
                ('kind', models.CharField(choices=[('standard', 'Standard'), ('copy', 'Copy'), ('contract', 'Contract')], default='standard', max_length=16)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('settings', django.contrib.postgres.fields.jsonb.JSONField(default=hourglass.campaigns.models.campaign_default_settings, null=True, verbose_name='JSON settings')),
                ('order', models.IntegerField(null=True, verbose_name='Purchase Order')),
                ('campaign_type', models.CharField(max_length=128, null=True, verbose_name='Campaign Type')),
                ('details', models.TextField(null=True, verbose_name='Campaign Details')),
                ('guarantees', models.TextField(null=True, verbose_name='Campaign Guarantees')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
            ],
            options={
                'verbose_name': 'Campaign',
                'verbose_name_plural': 'Campaigns',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RevenueSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Revenue')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenues', to='campaigns.Campaign')),
            ],
            options={
                'verbose_name': 'Revenue',
                'verbose_name_plural': 'Revenue',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JobTitlesSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Job Titles')),
                ('generated', models.PositiveSmallIntegerField(default=0, verbose_name='Leads Generated')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='campaigns.Campaign')),
            ],
            options={
                'verbose_name': 'Job Title',
                'verbose_name_plural': 'Job Titles',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='IntentFeedsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Intent topic')),
                ('generated', models.PositiveSmallIntegerField(default=0, verbose_name='Leads Generated')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intents', to='campaigns.Campaign')),
            ],
            options={
                'verbose_name': 'Intent Feed',
                'verbose_name_plural': 'Intent Feeds',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='IndustriesSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Industry')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industries', to='campaigns.Campaign')),
            ],
            options={
                'verbose_name': 'Industry',
                'verbose_name_plural': 'Industries',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GeolocationsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Geolocation title')),
                ('goal_per_geo', models.FloatField(default=0, verbose_name='Goal per Geo')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='geolocations', to='campaigns.Campaign')),
                ('geolocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='references.Geolocations')),
            ],
            options={
                'verbose_name': 'Geolocation',
                'verbose_name_plural': 'Geolocations',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CustomQuestionsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('answer', models.TextField(verbose_name='Answer')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cqs', to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CompanySizeSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Company Size')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='campaigns.Campaign')),
            ],
            options={
                'verbose_name': 'Company Size',
                'verbose_name_plural': 'Companies Sizes',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CampaignsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('integration', models.CharField(choices=[('salesforce', 'Salesforce'), ('marketo', 'Marketo'), ('hub_spot', 'HubSpot'), ('integrate', 'Integrate'), ('lolagrove', 'Lolagrove')], default='salesforce', max_length=16)),
                ('pacing', models.CharField(choices=[('even', 'Even'), ('front-load', 'Front-Load')], default='even', max_length=16)),
                ('leads_goal', models.PositiveIntegerField(verbose_name='Leads goal')),
                ('leads_generated', models.PositiveIntegerField(verbose_name='Leads Generated')),
                ('velocity', models.PositiveSmallIntegerField(verbose_name='Velocity')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='campaigns.Campaign')),
                ('campaign_pos_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='references.CampaignTypes')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BANTQuestionsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Answer')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bants', to='campaigns.Campaign')),
            ],
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AssetsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('name', models.CharField(max_length=200, verbose_name='Asset Name')),
                ('landing_page', models.FileField(upload_to='', verbose_name='Landing Page')),
                ('velocity_koeff', models.FloatField(default=1.0)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='campaigns.Campaign')),
                ('titles', models.ManyToManyField(blank=True, to='references.JobTitles')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
    ]
