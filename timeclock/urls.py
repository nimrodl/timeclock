from django.conf import settings
from django.urls import path, include
from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView

from . import views, forms

app_name = 'timeclock'
urlpatterns = [
        path('', views.UserEventView.as_view(), name='user'),
        path('user/', views.UserEventView.as_view(), name='user'),
        path('summary/', views.SummaryView.as_view(), name='summary'),
        path('card/<int:cardnum>/', views.card, name='card'),
        path('clockIn', views.clockIn, name='clockIn'),
        path('clockOut', views.clockOut, name='clockOut'),
        path('login/', LoginView.as_view( authentication_form=forms.MyLoginForm,), name='login',),
        path('logout/', LogoutView.as_view( next_page='/timeclock/user' ), name='logout',),
]


