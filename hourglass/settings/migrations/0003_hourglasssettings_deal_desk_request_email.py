# Generated by Django 3.2.6 on 2022-06-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20210714_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourglasssettings',
            name='deal_desk_request_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='DealDesk Request Email'),
        ),
    ]
