# Generated by Django 3.0.5 on 2021-06-13 15:06

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_fsm
import model_clone.mixins.clone


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0009_abmsection_installbasesection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='abmsection',
            options={'verbose_name': 'ABM', 'verbose_name_plural': 'ABM'},
        ),
        migrations.AlterModelOptions(
            name='bantquestionssection',
            options={'verbose_name': 'BANT Question', 'verbose_name_plural': 'BANT Questions'},
        ),
        migrations.AlterModelOptions(
            name='customquestionssection',
            options={'verbose_name': 'Custom Question', 'verbose_name_plural': 'Custom Questions'},
        ),
        migrations.CreateModel(
            name='NurturingSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('execution_time', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=256, verbose_name='Type')),
                ('assets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.AssetsSection')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nurturings', to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LeadCascadeProgramSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('execution_time', models.IntegerField(default=0)),
                ('percent', models.FloatField(default=0)),
                ('name', models.CharField(max_length=256, verbose_name='Leads Description')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_cascades', to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FairTradeSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('execution_time', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=256, verbose_name='Treat Desctiption')),
                ('value', models.CharField(max_length=256, verbose_name='Value')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fair_trades', to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CreativesSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('new', 'new'), ('running', 'running'), ('pause', 'pause'), ('stopped', 'stopped')], default='new', max_length=50)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('execution_time', models.IntegerField(default=0)),
                ('name', models.EmailField(max_length=254, verbose_name='email')),
                ('value', models.TextField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creatives', to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
    ]
