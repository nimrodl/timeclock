from django.conf import settings
from django.urls import path, include
from django.contrib import auth
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'timeclock'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('user/', views.UserEventView.as_view(), name='user'),
        path('summary/', views.SummaryView.as_view(), name='summary'),
        path('card/<int:cardnum>/', views.card, name='card'),
        path('clockIn', views.clockIn, name='clockIn'),
        path('clockOut', views.clockOut, name='clockOut'),
]


