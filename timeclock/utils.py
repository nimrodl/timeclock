from django.urls import reverse
from datetime import datetime, timedelta
from calendar import *
from .models import Event

class Calendar(HTMLCalendar):
        def __init__(self, year=None, month=None):
                self.year = year
                self.month = month
                super(Calendar, self).__init__()

        # formats a day as a td
        # filter events by day
        def formatday(self, day, events):
                events_per_day = events.filter(date=day).order_by('user','time_in')
                d = ''
                for event in events_per_day:
                    time_in = event.time_in if event.time_in else '<span style="color:red">None</span>'
                    time_out = event.time_out if event.time_out else '<span style="color:red">None</span>'
                    d += f'<li> {event.user.name} {time_in} - {time_out} </li>'

                cls = f'class="{self.cssclasses[day.weekday()]}"'
                if day.month != self.month:
                    cls = 'class="other"'
                return f"<td {cls}><span class='date'>{day.day}</span><ul> {d} </ul></td>"

        # formats a week as a tr 
        def formatweek(self, theweek, events):
                week = ''
                #pop sunday off so we don't send that to be formatted
                day = theweek.pop()
                #format days
                for d in theweek:
                        week += self.formatday(d, events)

                # get pay data
                pay = events.week_pay(date=theweek[0])
                sun = ""
                for user, hours in pay.items():
                    ot=f'- ot: {hours["ot"]}' if hours["ot"] else ""
                    sun += f'<li> {hours["name"]} - reg: {hours["reg"]} {ot} </li>'
                week += f"<td class='{self.cssclasses[6]}'><span class='date'>{day.day}</span><ul> {sun} </ul></td>"

                return f'<tr> {week} </tr>'

        def formatmonthname(self, theyear, themonth, withyear=True):
            prevu = f"{reverse('timeclock:calendar')}?{self.context['prev_month']}"
            nextu = f"{reverse('timeclock:calendar')}?{self.context['next_month']}"
            prevm = f'<a class="btn btn-info" href="{prevu}"> Previous Month </a>'
            nextm = f'<a class="btn btn-info" href="{nextu}"> Next Month </a>'
            if withyear:
                s = '%s %s' % (month_name[themonth], theyear)
            else:
                s = '%s' % month_name[themonth]
            return '<tr><th>%s</th><th colspan="5" class="%s">%s</th><th>%s</th></tr>' % (
                prevm, self.cssclass_month_head, s, nextm)

        # formats a month as a table
        # filter events by year and month
        def formatmonth(self, withyear=True, context=None):
            self.context=context

            cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
            cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
            cal += f'{self.formatweekheader()}\n'
            for week in self.monthdatescalendar(self.year, self.month):
                cal += f'{self.formatweek(week, context["object_list"])}\n'
            return cal


