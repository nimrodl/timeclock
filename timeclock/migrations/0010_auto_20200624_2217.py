# Generated by Django 3.0.7 on 2020-06-25 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeclock', '0009_auto_20200624_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='hours',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
