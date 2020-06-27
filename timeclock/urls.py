from django.conf import settings
from django.urls import path, include, reverse_lazy
from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView

from . import views, forms

app_name = 'timeclock'
urlpatterns = [
        path('', views.UserEventView.as_view(), name='user'),
        path('card/<int:cardnum>/', views.card, name='card'),
        path('clockIn', views.clockIn, name='clockIn'),
        path('clockOut', views.clockOut, name='clockOut'),
        path('login/', LoginView.as_view( authentication_form=forms.MyLoginForm,), name='login',),
        path('logout/', LogoutView.as_view( next_page=reverse_lazy('timeclock:user')), name='logout',),
]


