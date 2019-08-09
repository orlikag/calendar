import functions as f
from functions import Event


INCLUDE_MANUAL_EXAMPLE = True

# open the data base
cal = f.Main_Calendar("demoDB.csv")

# print the week of the 7/8/2019
# you can choose any day of the week, and it will print the week sunday to saturday
cal.print_week("7/8/2019")

# creating new event
if INCLUDE_MANUAL_EXAMPLE:
    start = f.time_format(f.get_date("start"), f.get_time("start"))
    check_end = False
    while not check_end:
        end = f.time_format(f.get_date("end"), f.get_time("end"))
        check_end = f.date_validation(start, end)
    title = input("Title: ")
    event_type = input("Event type: ")
    price = input("Price: ")
    invitees = input("Invitees: ")
    location = input("Location: ")
    event = f.Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
    cal.set_event(event)

    # print the week of 7/8/2019
    cal.print_week("7/8/2019")

    # print the event we created
    print(event)

    # pause execution for demo
    _ = input("press enter to continue")

    # update the new event date from 7/8/2019 to 8/8/2019
    # print updated event
    # print updated week
    cal.update_event(start, end, title, start=f.time_format("8/8/2019", "17:00"), end=f.time_format("8/8/2019", "17:30"))
    print(cal.get_event(f.time_format("8/8/2019", "17:00"), f.time_format("8/8/2019", "17:30"), title))
    cal.print_week("8/8/2019")

# pause execution for demo
_ = input("press enter to continue")

# delete event: "friend hangouts"
cal.drop_event(cal.get_event(f.time_format("4/8/2019", "20:00"), f.time_format("4/8/2019", "21:00"), "pilates"))
cal.print_week("4/8/2019")

# pause execution for demo
_ = input("press enter to continue")

# add new events
title = "Rotem's birthday"
event_type = "pub"
price = 150
start = f.time_format("8/8/2019", "20:00")
end = f.time_format("8/8/2019", "23:30")
invitees = None
location = "Rosa Parks"
event1 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
cal.set_event(event1)


title = "friends hangout"
event_type = "pub"
price = 150
start = f.time_format("9/8/2019", "20:00")
end = f.time_format("9/8/2019", "23:30")
invitees = None
location = "Double Standart"
event2 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
cal.set_event(event2)


title = "Pilates"
event_type = "studio"
price = 50
start = f.time_format("9/8/2019", "8:00")
end = f.time_format("9/8/2019", "9:00")
invitees = None
location = "Studio SHINE"
event3 = Event(start, end, title, event_type=event_type, price=price, invitees=invitees, location=location)
cal.set_event(event3)

cal.print_week("7/8/2019")

# pause execution for demo
_ = input("press enter to continue")

# add event without price
title = "she codes"
event_type = "she codes"
start = f.time_format("7/8/2019", "18:00")
end = f.time_format("7/8/2019", "21:00")
invitees = None
location = "IBM"
event5 = Event(start, end, title, event_type=event_type, invitees=invitees, location=location)
cal.set_event(event5)

print(cal.get_event(start, end, title))

# pause execution for demo
_ = input("press enter to continue")

# print one day: Friday, 12/8/2019
cal.print_day("7/8/2019")

# pause execution for demo
_ = input("press enter to continue")

# print 6 months graph of all expenses
cal.print_monthly_overview(None)

# print 6 months graph of "pub" type expenses
cal.print_monthly_overview("pub")

# print this month expenses devided by category
cal.month_overview_by_types()

# save the calendar
cal.save_calendar()