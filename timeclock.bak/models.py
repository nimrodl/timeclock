from django.db import models
from django.db.models import DateTimeField, DateField, ExpressionWrapper, F, Count
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cardnum = models.IntegerField()
    def __str__(self):
        return self.user.username

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db).all()

class EventQuerySet(models.QuerySet):
    def all(self):
        qs = super(EventQuerySet, self).all()
        qs = qs.annotate_with_hours()
        qs = qs.annotate_with_date()
        return qs
    def annotate_with_hours(self):
        return self.annotate(hours=ExpressionWrapper(F('time_out')-F('time_in'), output_field=DateTimeField()))
    def annotate_with_date(self):
        return self.annotate(date=F('time_in'))

class Event(models.Model):
    objects = EventManager.from_queryset(EventQuerySet)()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.user.username 
    class Meta:
        ordering = ['time_in']


