from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Sum
import datetime
from dateutil.relativedelta import *
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib import messages
import calendar

from .utils import Calendar
from .models import User, Event


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('timeclock:login')
    model = Event
    template_name = 'timeclock/calendar.html'
    def get_time(self):
        return timezone.localtime().replace(second=0,microsecond=0).time()

    def clockIn(self):
        try:
            latest = self.request.user.event_set.latest('date','time_in')
            if latest.date == timezone.localdate() and latest.time_out == None:
                raise Event.DoesNotExist
            else:
                self.request.user.event_set.create(
                        time_in=self.get_time()
                        )
        except Event.DoesNotExist as e:
            messages.error(self.request, "You are already clocked in today without clocking out")

    def clockOut(self):
        try:
            latest = self.request.user.event_set.latest('date','time_in')
            if latest.date != timezone.localdate() or latest.time_out != None:
                raise Event.DoesNotExist
            else:
                latest.time_out = self.get_time()
                latest.save()
        except Event.DoesNotExist:
            messages.error(self.request, "You are trying to clock out, but there is no clock in")
            #self.request.user.event_set.create(
            #        time_out=self.get_time()
            #        )

    def get_queryset(self):
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        qs = Event.objects.filter(date__in = Calendar().itermonthdates(d.year,d.month))
        queryset = qs if self.request.user.is_staff \
            else qs.filter(user = self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        if self.request.META['PATH_INFO'] == '/clockIn/':
            self.clockIn()
        if self.request.META['PATH_INFO'] == '/clockOut/':
            self.clockOut()
        context = super().get_context_data(**kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        p = get_paydate(self.request.GET.get('paydate', None))
        context['prev_month'] = prev_month(d) +"&"+cur_pay(p)
        context['next_month'] = next_month(d) +"&"+cur_pay(p)
        context['prev_pay'] = cur_month(d)+"&"+prev_pay(p)
        context['next_pay'] = cur_month(d)+"&"+next_pay(p)
        context['pay_start'] = get_paydate(str(p)) #+ " - " + str(get_paydate(str(p+datetime.timedelta(13))))
        context['pay_end'] = context['pay_start']+datetime.timedelta(13)
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True, context=context)
        context['calendar'] = mark_safe(html_cal)
        # get summary data for payroll section below the calendar
        user_list = User.objects.filter(is_active=True, is_staff=False).order_by('last_name') if self.request.user.is_staff \
                else User.objects.filter(id = self.request.user.id)
        context['summary'] = {}
        for user in user_list:
            context['summary'][user.id]={
                    'paydata': Event.objects.filter(user = user.id).paydata(date=p),
                    'name': user.name,
                    }
        return context

    def render_to_response(self, context, **response_kwargs):
            response = super().render_to_response(
                    context, **response_kwargs
            )
            if not messages.get_messages(self.request) and (self.request.META['PATH_INFO'] == '/clockIn/' or self.request.META['PATH_INFO'] == '/clockOut/'):
                response['Refresh'] = "4;url=" + reverse('timeclock:logout')
            return response


def get_paydate(req):
    if req:
        date = datetime.date.fromisoformat(req)
    else:
        # date = previous monday
        date = timezone.localdate() + relativedelta(weekday=MO, weeks=-1)
    # first pay period ever
    start = datetime.date(2020,6,8)
    # set date to start of payperiod
    date = date-datetime.timedelta(7) if ((date-start).days % 14) ==7 else date
    return date

def cur_pay(date):
    return 'paydate='+str(date)

def prev_pay(date):
    return 'paydate='+str(date - datetime.timedelta(14))

def next_pay(date):
    return 'paydate='+str(date + datetime.timedelta(14))


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def cur_month(d):
    month = 'month=' + str(d.year) + '-' + str(d.month)
    return month

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
