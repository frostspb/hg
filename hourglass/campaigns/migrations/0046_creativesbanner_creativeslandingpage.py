# Generated by Django 3.2.6 on 2022-01-12 16:05

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_fsm
import model_clone.mixins.clone


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0045_nurturingsection_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreativesLandingPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('running', 'running'), ('pause', 'pause')], default='running', max_length=50, verbose_name='Status')),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('execution_time', models.IntegerField(default=0)),
                ('landing_page', models.FileField(blank=True, null=True, upload_to='')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landings', to='campaigns.campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CreativesBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', django_fsm.FSMField(choices=[('running', 'running'), ('pause', 'pause')], default='running', max_length=50, verbose_name='Status')),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('execution_time', models.IntegerField(default=0)),
                ('banner', models.FileField(blank=True, null=True, upload_to='')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='campaigns.campaign')),
            ],
            options={
                'abstract': False,
            },
            bases=(model_clone.mixins.clone.CloneMixin, models.Model),
        ),
    ]
