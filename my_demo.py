import functions as f
from functions import Main_Calendar
from functions import Event

# open the data base
calendar = Main_Calendar("demoDB.csv")

# print the week of the 7/7/2019
# you can choose any day of the week, and it will print the week sunday to saturday
calendar.print_week("7/7/2019")

# creating new event
start = f.time_format(f.get_date("start"), f.get_time("start"))
end = f.time_format(f.get_date("end"), f.get_time("end"))
title = input("Title: ")
event_type = input("Event type:: ")
price = int(input("Price: "))
invitees = input("Invitees: ")
location = input("Location: ")
event = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
calendar.set_event(event)

# print the week of 7/7/2019
calendar.print_week("7/7/2019")

# print the event we created
print(event)

# update the new event date from 7/7/2019 to 8/7/2019
# print updated event
# print updated week
calendar.update_event(start, end, title, start=f.time_format("8/7/2019", "17:00"), end=f.time_format("8/7/2019", "17:30"))
print(calendar.get_event(f.time_format("8/7/2019", "17:00"), f.time_format("8/7/2019", "17:30"), title))
calendar.print_week("8/7/2019")

# delete event: "friend hangouts"
calendar.drop_event(calendar.get_event(f.time_format("8/7/2019", "20:00"), f.time_format("8/7/2019", "23:30"), "friends hangout"))
calendar.print_week("8/7/2019")

# add new events
title = "Rotem's birthday"
event_type = "bar"
price = 150
start = f.time_format("8/7/2019", "20:00")
end = f.time_format("8/7/2019", "23:30")
invitees = None
location = "Rosa Parks"
event1 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
calendar.set_event(event1)


title = "friends hangout"
event_type = "bar"
price = 150
start = f.time_format("10/7/2019", "20:00")
end = f.time_format("10/7/2019", "23:30")
invitees = None
location = "Double Standart"
event2 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
calendar.set_event(event2)


title = "Pilates"
event_type = "studio"
price = 50
start = f.time_format("12/7/2019", "8:00")
end = f.time_format("12/7/2019", "9:00")
invitees = None
location = "Studio SHINE"
event3 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
calendar.set_event(event3)


title = "Friday Dinner"
event_type = "restaurant"
price = 150
start = f.time_format("12/7/2019", "20:00")
end = f.time_format("12/7/2019", "22:00")
invitees = None
location = "התרנגול הכחול"
event4 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
calendar.set_event(event4)

calendar.print_week("7/7/2019")

# add event without price
title = "After dinner"
event_type = "bar"
start = f.time_format("12/7/2019", "22:00")
end = f.time_format("12/7/2019", "23:30")
invitees = None
location = "Rosa Parks"
event5 = Event(start, end, title, event_type=event_type, invitees=invitees, location=location)
calendar.set_event(event5)

print(calendar.get_event(start, end, title))

# print one day: Friday, 12/7/2019
calendar.print_day("12/7/2019")

# save the calendar
calendar.save_calendar()