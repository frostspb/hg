# Generated by Django 3.2.6 on 2021-11-23 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0044_alter_assetssection_titles'),
        ('references', '0014_topics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bantanswer',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='bantquestion',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='customanswer',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='customquestion',
            name='owner',
        ),
        migrations.AddField(
            model_name='bantquestion',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.campaign'),
        ),
        migrations.AddField(
            model_name='customquestion',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.campaign'),
        ),
    ]
