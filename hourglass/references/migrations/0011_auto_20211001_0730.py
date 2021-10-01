# Generated by Django 3.2.6 on 2021-10-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0010_alter_bantquestion_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='bantquestion',
            name='pos',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bantquestion',
            name='kind',
            field=models.CharField(choices=[('budget', 'Budget'), ('authority', 'Authority'), ('need', 'Need'), ('time', 'Time')], default='budget', max_length=16),
        ),
    ]
