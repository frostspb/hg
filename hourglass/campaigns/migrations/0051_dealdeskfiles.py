# Generated by Django 3.2.6 on 2022-06-18 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0050_dealdesk_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealDeskFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('deal_desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.dealdesk')),
            ],
        ),
    ]
