from django.conf import settings
from django.urls import path, include, reverse_lazy
from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView

from . import views, forms

app_name = 'timeclock'
urlpatterns = [
        path('', views.CalendarView.as_view(), name='calendar'),
        path('clockIn/', views.clockIn.as_view(), name='clockIn'),
        path('clockOut/', views.clockOut.as_view(), name='clockOut'),
        path('login/', LoginView.as_view( authentication_form=forms.MyLoginForm,), name='login',),
        path('logout/', LogoutView.as_view( next_page='/'), name='logout',),
]


