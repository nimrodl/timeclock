from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models import DateField, FloatField, ExpressionWrapper, F, Case, When, Sum, Value
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from dateutil.relativedelta import *

class User(AbstractUser):
    cardnum = models.IntegerField(blank=True, null=True, unique=True)
    pin = models.IntegerField(unique=True)
    REQUIRED_FIELDS = ['pin']

class EventQuerySet(models.QuerySet):
    def all(self):
        qs = super(EventQuerySet, self).all()
        return qs
    @property
    def total(self):
        if (self.aggregate(total=Sum('hours')))['total']:
            return round((self.aggregate(total=Sum('hours')))['total'],2) 
        else:
            return 0
    @property
    def reg(self):
        return 40 if self.total>40 else self.total
    @property
    def ot(self):
        return round(self.total-40,2) if self.total>40 else 0
    @property
    def weeks(self):
        return [
                self.week(-2),
                self.week(-1),
                self.week(0),
                ]
    def week(self, index=0, day=timezone.now()):
        sun = (day + relativedelta(weekday=SU, weeks=-1+index)).date()
        sat = (day + relativedelta(weekday=SA, weeks=-0+index)).date()
        qs = self.filter(date__range=[sun,sat])
        return qs
    @property
    def paydata(self):
        out = { 'reg': self.week(-2).reg + self.week(-1).reg,
                'ot': round(self.week(-2).ot + self.week(-1).ot,2),
                'total': self.week(-2).total + self.week(-1).total,
                }
        return out

class Event(models.Model):
    objects = models.Manager.from_queryset(EventQuerySet)()
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    date = models.DateField(default=datetime.date.today)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    hours = models.FloatField(null=True, blank=True, editable=False)
    @property
    def get_hours(self):
        return round(self.hours,2) if self.hours else ""
    def __str__(self):
        return self.user.first_name + " - " + str(self.date)
    class Meta:
        ordering = ['date', 'time_in', 'time_out']


@receiver(models.signals.pre_save, sender=Event)
def save_Event(sender, instance, **kwargs):
    if instance.time_in and instance.time_out:
        start = datetime.time(7,45,0)
        time_in = start if instance.time_in < start else instance.time_in
        instance.hours = (
                    datetime.datetime.combine(instance.date,instance.time_out) - 
                    datetime.datetime.combine(instance.date,time_in)
                    ).total_seconds() / 3600
    else:
        instance.hours = None

