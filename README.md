# timeclock
timeclock app using django

This project came about because I was looking for a simple timeclock to have employees clock in and out each day and I couldn't find anything I liked.

This is still very early development and is my first attempt in django.

Things that work:
 - logging in
 - clocking in and out
 - displaying the current and previous 2 weeks of time entries
 - displaying summary of the previous 2 weeks of entries for payroll purposes including accountig for overtime over 40 hours per week
 - displaying all user summary information for all users if current user is_staff
 - users have mandatory pin field that can be used as sole identifier (no user/pass) using /timeclock/login/
 - event.html style is updated, but can use some improvement from someone who is better at UI than I am
 
 Things to do:
  - anything else I think of 
