import datetime
import functions as f


c = f.Main_Calendar("CalendarDB.csv")
c.print_week("24/5/2019")
#event_list = c.get_month("5", "2019").values.tolist()



s_date = "8/5/2019"
s_time = "18:00"
start = f.time_format(s_date, s_time)
e_date = "8/5/2019"
e_time = "21:00"
end = f.time_format(e_date, e_time)
title = "she codes"
location = "lalalalala"
event = f.Event(start, end, title, location=location)
c.create_event(event)
print(c)
c.save_calendar()

print(c)

event1 = event.update(title="lalala")
c.set_event(event1)
c.save_calendar()


title = "meni"
event_type = "nails"
price = "100"
s_date = "01/05/2019"
s_time = "16:00"
start = f.time_format(s_date, s_time)
e_date = "01/05/2019"
e_time = "17:00"
end = f.time_format(e_date, e_time)
invitees = None
location = "por la vida"
repeat = None

event1 = f.Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
c.set_event(event1)

s_date = input("start date: ")
e_date = input("end date: ")
events = c.period(s_date, e_date)
print(events)
