# Generated by Django 3.2.6 on 2021-09-26 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0008_auto_20210803_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurturingStages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Type')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Nurturing Stage',
                'verbose_name_plural': 'Nurturing Stages',
            },
        ),
    ]
