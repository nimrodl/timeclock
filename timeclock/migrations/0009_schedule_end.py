# Generated by Django 3.0.7 on 2020-09-05 19:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('timeclock', '0008_auto_20200905_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='end',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
