from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Sum
import datetime

from .models import User, Event

class IndexView(generic.ListView):
    model = User
    template_name = 'timeclock/index.html'

class UserEventView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'timeclock/events.html'
    def get_queryset(self):
        queryset = Event.objects.filter(user = self.request.user.id )
        return queryset

class SummaryView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'timeclock/summary.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = User.objects.all() if self.request.user.is_staff else User.objects.filter(id = self.request.user.id)
        context['data_list']={}
        for user in user_list:
            context['data_list'][user.first_name]=Event.objects.filter(user = user.id).paydata
        return context


def card(request, cardnum):
    user = get_object_or_404(User, staff__cardnum=cardnum)
    return HttpResponseRedirect(reverse('timeclock:user'))

@login_required
def clockIn(request):
    user = get_object_or_404(User, pk=request.user.id)
    user.event_set.create(
            time_in=timezone.localtime().replace(second=0,microsecond=0).time()
            )
    return HttpResponseRedirect(reverse('timeclock:user'))

@login_required
def clockOut(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user.event_set.all():
        latest = user.event_set.latest('date','time_in')
        if latest.time_out:
            user.event_set.create(
                    time_out=timezone.localtime().replace(second=0,microsecond=0).time()
                    )
        else:
            latest.time_out = timezone.localtime().replace(second=0,microsecond=0).time()
            latest.save()
    return HttpResponseRedirect(reverse('timeclock:user'))

