from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Sum
import datetime

from .models import User, Event

class UserEventView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('timeclock:login')
    template_name = 'timeclock/events.html'
    def get_queryset(self):
        queryset = Event.objects.filter(user = self.request.user.id )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = User.objects.all() if self.request.user.is_staff else User.objects.filter(id = self.request.user.id)
        context['summary'] = {}
        for user in user_list:
            context['summary'][user.first_name]=Event.objects.filter(user = user.id).paydata
        return context

class clockIn(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('timeclock:login')
    def get(self, request, *args, **kwargs):
        self.request.user.event_set.create(
                time_in=timezone.localtime().replace(second=0,microsecond=0).time()
                )
        return HttpResponseRedirect(reverse('timeclock:logout'))

class clockOut(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('timeclock:login')
    def get(self, request, *args, **kwargs):
        try:
            latest = self.request.user.event_set.latest('date','time_in')
            if latest.date != timezone.localdate() or latest.time_out != None:
                raise Event.DoesNotExist
            else:
                latest.time_out = timezone.localtime().replace(second=0,microsecond=0).time()
                latest.save()
        except Event.DoesNotExist:
            self.request.user.event_set.create(
                    time_out=timezone.localtime().replace(second=0,microsecond=0).time()
                    )
        return HttpResponseRedirect(reverse('timeclock:logout'))

