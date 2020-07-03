from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from dateutil.relativedelta import *

class User(AbstractUser):
    cardnum = models.IntegerField(blank=True, null=True, unique=True)
    pin = models.IntegerField(unique=True)
    REQUIRED_FIELDS = ['pin']
    @property
    def name(self):
        return self.first_name + " " + self.last_name

class EventQuerySet(models.QuerySet):
    def all(self):
        qs = super(EventQuerySet, self).all()
        return qs
    @property
    def total(self):
        length = self.aggregate(length=models.Sum('length'))['length']
        if length:
            return round(length.total_seconds()/3600,2)
        else:
            return 0
    @property
    def reg(self):
        return 40 if self.total>40 else self.total
    @property
    def ot(self):
        return round(self.total-40,2) if self.total>40 else 0
    def week(self, index=0, day=timezone.localdate()):
        sun = (day + relativedelta(weekday=MO, weeks=-1+index))
        sat = (day + relativedelta(weekday=SU, weeks=-1+index))
        qs = self.filter(date__range=[sun,sat])
        return qs
    @property
    def paydata(self, date=timezone.localdate()):
        first = date + relativedelta(weekday=MO, weeks=-3)
        last = date + relativedelta(weekday=SU, weeks=-1)
        out = { 'reg': self.week(day=first).reg + self.week(day=last).reg,
                'ot': round(self.week(day=first).ot + self.week(day=last).ot,2),
                'total': round(self.week(day=first).total + self.week(day=last).total,2),
                'first': first,
                'last': last,
                }
        return out
    def week_pay(self, date=timezone.localdate()):
        out={}
        for user in self.week(day=date).values('user').order_by('user'):
            user_week = self.week(day=date).filter(user=user['user'])
            user_pay = user_week.week(day=date)
            out[ user['user'] ]={
                    'name': User.objects.get(pk=user['user']).name,
                    'reg': user_pay.reg,
                    'ot': user_pay.ot,
                    }
        return out

class Event(models.Model):
    objects = models.Manager.from_queryset(EventQuerySet)()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    length = models.DurationField(null=True, blank=True, editable=False)
    def get_hours(self):
        return round(self.length.total_seconds()/3600,2) if self.length else ""
    get_hours.short_description="hours"
    get_hours.admin_order_field="length"
    def __str__(self):
        return self.user.name + " - " + str(self.date)
    class Meta:
        ordering = ['date', 'time_in', 'time_out']


@receiver(models.signals.pre_save, sender=Event)
def save_Event(sender, instance, **kwargs):
    if instance.time_in and instance.time_out:
        start = datetime.time(7,45,0)
        time_in = start if instance.time_in < start else instance.time_in
        instance.length = (
                    datetime.datetime.combine(instance.date,instance.time_out) - 
                    datetime.datetime.combine(instance.date,time_in)
                    )
    else:
        instance.length = None

