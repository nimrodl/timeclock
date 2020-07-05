# timeclock
timeclock app using django

This project came about because I was looking for a simple timeclock to have employees clock in and out each day and I couldn't find anything I liked.

This is still very early development and is my first project in django.

Things that work:
 - logging in using pin (not synchronized, but same as other system in use)
 - clocking in and out
 - calendar display
 - totals for pay period including OT (calculated as >40 hours per week)
 - displaying all information for all users if current user is_staff
 - users have mandatory pin field that can be used as sole identifier (no user/pass needed) using /login/
 
 Things to do:
  - anything else I think of 
