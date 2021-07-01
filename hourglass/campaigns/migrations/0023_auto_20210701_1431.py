# Generated by Django 3.0.5 on 2021-07-01 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0006_companysize'),
        ('campaigns', '0022_auto_20210701_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='companysizesection',
            name='company_size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='references.CompanySize', verbose_name='Company Size'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companysizesection',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='revenuesection',
            name='revenue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revens', to='references.Revenue', verbose_name='Revenue Title'),
        ),
    ]
