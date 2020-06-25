from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Sum
import datetime
from dateutil.relativedelta import *

from .models import User, Event

class IndexView(generic.ListView):
    model = User
    template_name = 'timeclock/index.html'

def get_events_this_week(date):
    sun = date + relativedelta(weekday=SU, weeks=-1)
    sat = date + relativedelta(weekday=SA)
    return Event.objects.filter(date__gte=sun).filter(date__lte=sat)

def get_events_last_week(date):
    sun = date + relativedelta(weekday=SU, weeks=-2)
    sat = date + relativedelta(weekday=SA, weeks=-1)
    return Event.objects.filter(date__gte=sun).filter(date__lte=sat)

class UserView(generic.ListView):
    model = Event
    template_name = 'timeclock/events.html'
    def get_queryset(self):
        queryset = Event.objects.filter(user = self.kwargs['user_id'] )
        return queryset
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['total']=(context['object_list'].aggregate(total=Sum('hours')))['total']
        context['uid']=self.kwargs['user_id']
        context['week1']=get_events_last_week(timezone.now())
        context['week1_total']=(context['week1'].aggregate(total=Sum('hours')))['total']
        context['week2']=get_events_this_week(timezone.now())
        context['week2_total']=(context['week2'].aggregate(total=Sum('hours')))['total']
        #context['total']=context['week1_total'] + context['week2_total']
        return context

def card(request, cardnum):
    user = get_object_or_404(User, staff__cardnum=cardnum)
    return HttpResponseRedirect(reverse('timeclock:user', args=(user.id,)))

def clockIn(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.event_set.create(
            time_in=timezone.localtime().replace(second=0,microsecond=0)
            )
    return HttpResponseRedirect(reverse('timeclock:user', args=(user_id,)))

def clockOut(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.event_set.all():
        latest = user.event_set.latest('date','time_in')
        if latest.time_out:
            user.event_set.create(
                    time_out=timezone.localtime().replace(second=0,microsecond=0)
                    )
        else:
            latest.time_out = timezone.localtime().replace(second=0,microsecond=0)
            latest.hours = (
                    latest.time_out - latest.time_in
                ).total_seconds() / 3600
            latest.save()
    return HttpResponseRedirect(reverse('timeclock:user', args=(user_id,)))

