from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from timeclock.models import Staff, Event

class EventInline(admin.TabularInline):
    model = Event
    extra = 1

class StaffInline(admin.TabularInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = [StaffInline, EventInline, ]

class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_in', 'time_out']
    list_filter = (
            'user',
            ('time_in', DateRangeFilter),
            )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
