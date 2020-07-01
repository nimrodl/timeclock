from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from timeclock.models import User, Event

class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    readonly_fields = ['get_hours']
    fields = ['date', 'time_in', 'time_out', 'get_hours']

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
            (None, {'fields':('pin','cardnum',)}),
            )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
            (None, {'fields':('first_name','last_name','pin','cardnum',)}),
            )
    inlines = [EventInline, ]

class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'time_in', 'time_out', 'get_hours']
    list_editable = ['user','date', 'time_in', 'time_out']
    list_filter = (
            'user',
            ('date', DateRangeFilter),
            )

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
