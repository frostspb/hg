# Generated by Django 3.2.6 on 2021-11-11 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0012_partofmap'),
        ('campaigns', '0041_auto_20211104_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysizesection',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='campaigns.campaign'),
        ),
        migrations.AlterField(
            model_name='geolocationssection',
            name='geolocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='references.geolocations'),
        ),
        migrations.AlterField(
            model_name='revenuesection',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revenues', to='campaigns.campaign'),
        ),
    ]