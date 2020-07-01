# Generated by Django 3.0.7 on 2020-07-01 13:36

from django.db import migrations
import datetime 

def calc(apps, schema_edotor):
    Event = apps.get_model('timeclock', 'Event')
    start = datetime.time(7,45,0)
    for event in Event.objects.all():
        time_in = start if event.time_in < start else event.time_in
        event.length =  (
                datetime.datetime.combine(event.date,event.time_out) -
                datetime.datetime.combine(event.date,time_in) 
                )
        event.save()

class Migration(migrations.Migration):

    dependencies = [
        ('timeclock', '0004_event_length'),
    ]

    operations = [
            migrations.RunPython(calc)
    ]
