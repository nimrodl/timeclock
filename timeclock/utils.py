from datetime import datetime, timedelta
from calendar import HTMLCalendar, weekday
from .models import Event

class Calendar(HTMLCalendar):
        def __init__(self, year=None, month=None):
                self.year = year
                self.month = month
                super(Calendar, self).__init__()

        # formats a day as a td
        # filter events by day
        def formatday(self, day, events):
                events_per_day = events.filter(date__day=day).order_by('user','time_in')
                d = ''
                for event in events_per_day:
                    d += f'<li> {event.user.first_name} {event.time_in} - {event.time_out} </li>'

                if day != 0:
                        return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
                return '<td></td>'

        # formats a week as a tr 
        def formatweek(self, theweek, events):
                week = ''
                #pop sunday off so we don't send that to be formatted
                day = theweek.pop()
                #format days
                for d, weekday in theweek:
                        week += self.formatday(d, events)

                # get pay data for the full week (or at least the part of the week that falls in the current month
                sday = day[0] if day[0] else ''
                date = datetime(self.year, self.month, theweek[0][0] if theweek[0][0] else 1)
                pay = events.week_pay(date=date)
                sun = ""
                for user, hours in pay.items():
                    ot=f'- ot: {hours["ot"]}' if hours["ot"] else ""
                    sun += f'<li> {user} - reg: {hours["reg"]} {ot} </li>'
                week += f"<td class='sunday'><span class='date'>{sday}</span><ul> {sun} </ul></td>"

                return f'<tr> {week} </tr>'

        # formats a month as a table
        # filter events by year and month
        def formatmonth(self, withyear=True, event_list=Event.objects):
                events = event_list.filter(date__year=self.year, date__month=self.month)

                cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
                cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
                cal += f'{self.formatweekheader()}\n'
                for week in self.monthdays2calendar(self.year, self.month):
                        cal += f'{self.formatweek(week, events)}\n'
                return cal
