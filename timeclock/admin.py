from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from datetime import datetime, timedelta

from timeclock.models import User, Event, Schedule

class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    readonly_fields = ['get_hours']
    fields = ['date', 'time_in', 'time_out', 'get_hours']
    def get_queryset(self, request):
        qs = super(EventInline, self).get_queryset(request)
        return qs.filter(date__gte=datetime.now()-timedelta(days=20))

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
    list_display_links = ['user']
    list_editable = ['date', 'time_in', 'time_out']
    list_filter = (
            'user',
            ('date', DateRangeFilter),
            )

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Schedule)
