# Generated by Django 3.2.6 on 2021-09-24 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0008_auto_20210803_2000'),
        ('campaigns', '0029_alter_leadcascadeprogramsection_percent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=1024, null=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='campaigns.campaign')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='references.managers')),
            ],
        ),
    ]
