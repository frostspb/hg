# Generated by Django 3.2.6 on 2022-06-29 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0051_dealdeskfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealdesk',
            name='user_lead_type',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
