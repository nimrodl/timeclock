from django.conf import settings
from django.urls import path, include

from . import views

app_name = 'timeclock'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('user/<int:user_id>/', views.UserView.as_view(), name='user'),
        path('card/<int:cardnum>/', views.card, name='card'),
        path('user/<int:user_id>/clockIn', views.clockIn, name='clockIn'),
        path('user/<int:user_id>/clockOut', views.clockOut, name='clockOut'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
