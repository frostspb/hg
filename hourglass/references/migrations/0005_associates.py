# Generated by Django 3.0.5 on 2021-07-20 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0004_itcurated_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Associates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]