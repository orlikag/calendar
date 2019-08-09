import pandas as pd
import datetime
from calendar import monthrange, month_name
import matplotlib.pyplot as plt

timestamp_format = "%d/%m/%Y %H:%M"


# check if date is valid
def check_date(date):
    try:
        datetime.datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# check if time is valid
def check_time(time):
    try:
        datetime.datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False


# takes start/end and asks user for start/end date
def get_date(when):
    check = False
    while not check:
        date = input(f"{when} date: ")
        check = check_date(date)
        if not check:
            print("date should be in format: DD/MM/YYYY")
    return date


# takes start/end and asks user for start/end time
def get_time(when):
    check = False
    while not check:
        time = input(f"{when} time: ")
        check = check_time(time)
        if not check:
            print("time should be in format: HH:MM")
    return time


# check that events end after it starts
def date_validation(start, end):
    check = True
    if end < start:
        print ("End time should be after start time.")
        check = False
    return check


# gets date and time and returns it in Timestamp format
def time_format(date, time):
    day, month, year = date.split("/")
    hour, minute = time.split(":")
    date_time = pd.Timestamp(int(year), int(month), int(day), int(hour), int(minute))
    return date_time


# checks that price is a valid number
def check_valid_price(price):
    try:
        price = float(price)
        return True
    except ValueError:
        return False


class Event(object):

    def __init__(self, start, end, title, **kwargs):
        self.start = start
        self.end = end
        self.title = title
        self.event_type = None
        self.price = None
        self.input_price = None
        self.invitees = None
        self.location = None
        self.repeat = None
        self.index = None
        for key, value in kwargs.items():
            setattr(self, key, value)
        if self.input_price is None:
            self.input_price = self.price is not None

    def __str__(self):
        event_str = f"Title: {self.title}\nType: {self.event_type}\nPrice: {self.price}\n" \
            f"Start: {self.start}\n" \
            f"End: {self.end}\nInvitees: {self.invitees}\n" \
            f"Location: {self.location}\nRepeat: {self.repeat}"
        return event_str

    # converts event to dict variable
    def to_dict(self):
        event_dict = {'start': self.start, 'end': self.end, 'title': self.title, 'event_type': self.event_type,
                      'price': self.price, 'input_price': self.input_price, 'invitees': self.invitees, 'location': self.location,
                      'repeat': self.repeat}
        return event_dict

    # updates the variables in the event
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self


class Main_Calendar(object):

    def __init__(self, file_name):
        self.DB = pd.read_csv(file_name, encoding='utf-8', parse_dates=['start', 'end'], dayfirst=True)

    # take start time, end time and title of event and gives back the event from DB
    def get_event(self, start, end, title):
        my_event = self.DB[(self.DB.start == start) & (self.DB.end == end) & (self.DB.title == title)]
        return Event(**my_event.squeeze())

    def __str__(self):
        return self.DB.__str__()

    # takes event variable
    # if exist --> delete it
    # add to event to DB
    def create_event(self, event):
        if self.duplication_check(event):
            exist_event = self.get_event(event.start, event.end, event.title)
            self.drop_event(exist_event)
        self.set_event(event)

    # takes event
    # if event has no price -> set price as average price of the category (with check price)
    # add event to DB
    def set_event(self, event):
        event = self.check_price(event)
        self.DB = self.DB.append(pd.Series(data=event.to_dict()), ignore_index=True)

    # gets event
    # delete it from DB
    def drop_event(self, event):
        event_index = self.DB[(self.DB.start == event.start) & (self.DB.end == event.end) & (self.DB.title == event.title)].index[0]
        self.DB = self.DB.drop(event_index)

    # gets start time, end time, title
    # delete the original event
    # add to DB updated event
    def update_event(self, start_origin, end_origin, title_origin, **kwargs):
        event = self.get_event(start_origin, end_origin, title_origin)
        self.drop_event(event)
        event = event.update(**kwargs)
        self.set_event(event)

    # save DB to "demoDB1.csv"
    def save_calendar(self):
        self.DB.sort_values(['start', 'end'], inplace=True)
        self.DB.to_csv('demoDB1.csv', encoding='utf-8')

    # gets start date and end date
    # returns all event in this period
    def period(self, start, end):
        period_events = self.DB[(self.DB.start >= start) & (self.DB.start <= end)]
        return period_events, period_events["price"].sum()

    # gets date
    # returns all events in this day
    def get_day(self, start):
        end = start + datetime.timedelta(hours=23, minutes=59)
        return self.period(start, end)

    # gets month and year
    # returns akk events in this month
    def get_month(self, month, year):
        start = time_format(f"1/{month}/{year}", "00:00")
        end = time_format(f"{monthrange(int(year),int(month))[1]}/{month}/{year}", "23:59")
        return self.period(start, end)

    # gets event
    # returns True if it doesn't exist in DB or False otherwise
    def duplication_check(self, event):
        exist = self.DB[(self.DB.start == event.start) & (self.DB.end == event.end) & (self.DB.title == event.title)] is not None
        return exist

    # gets event
    # if event doesn't have price, set price as average price of all events from the same type
    def check_price(self, event):
        if not event.input_price:
            event.update(price=self.calculate_average_price(event.event_type))
        elif not check_valid_price(event.price):
            event.update(price=self.calculate_average_price(event.event_type), input_price=False)
        return event

    # gets event type
    # returns the average price of all events from the same type
    # (only those where price was given by the user)
    def calculate_average_price(self, event_type):
        all_events = self.DB[(self.DB.event_type == event_type) & (self.DB.input_price)]
        return all_events["price"].mean()

    # gets date
    # print all the event in this day and the total outcome
    def print_day(self, day):
        if type(day) is not pd.Timestamp:
            day = time_format(day, "00:00")
        event_list, total_price = self.get_day(day)
        event_list = list(event_list.values)
        print(day.strftime("%A"), day.strftime("%d/%m/%Y"))
        print("===================")
        print(f"Total: {total_price}")
        print("-------------------")
        for event in event_list:
            print(f"{event[0].strftime(timestamp_format)} - {event[1].strftime(timestamp_format)}    {event[2]}")
        print("")

    # gets date
    # for each day of the week -> prints all the event of these day and the total outcome of the day
    def print_week(self, day):
        total_outcome = 0
        given_day = time_format(day, "00:00")
        today = given_day - datetime.timedelta(days=int(given_day.strftime("%w")))
        for i in range(7):
            self.print_day(today)
            today += datetime.timedelta(days=1)

    # gets event type
    # if event-type is None -> prints graph af all expenses in the last 6 months
    # otherwise -> prints graph of all expenses of this type in the last 6 months
    def print_monthly_overview(self, event_type):
        today = datetime.datetime.today()
        current_month = today.month
        current_year = today.year
        months = []
        print_months = []
        for m in range(6):
            months.append((current_month,current_year))
            print_months.append(f'{current_month}, {current_year}')
            if current_month == 1:
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1
        if event_type is None:
            expenses = self.monthly_overview_all_event_types(months)
            event_type = "all events"
        else:
            expenses = self.monthly_overview_one_type(months, event_type)
        plt.bar(print_months[::-1], expenses[::-1])
        plt.xlabel('Months')
        plt.ylabel(event_type)
        plt.title(f'Expense {print_months[-1]} - {print_months[0]}:')
        plt.show()

    # gets array of 6 months
    # returns array of total outcome for each month
    def monthly_overview_all_event_types(self, months):
        expenses = []
        for month, year in months:
            _, events_sum = self.get_month(month, year)
            expenses.append(int(events_sum))
        return expenses

    # gets array of 6 months and event type
    # returns array of total outcome for each months for events of the given type
    def monthly_overview_one_type(self, months, event_type):
        expenses = []
        for month, year in months:
            events, _ = self.get_month(month, year)
            expenses.append(events[events.event_type == event_type]['price'].sum())
        return expenses

    # prints pie graph of all the expenses this months divided by categories
    def month_overview_by_types(self):
        today = datetime.datetime.today()
        events, _ = self.get_month(today.month, today.year)
        types = list(dict.fromkeys(list(events.event_type)))
        expenses = []
        for t in types:
            expenses.append(events[events.event_type == t]['price'].sum())
        plt.pie(expenses, labels=expenses, autopct='%1.1f%%', shadow=True)
        plt.legend(types, loc='lower right')
        plt.title("Expenses by category this month:")
        plt.show()




#    @staticmethod
#    def events_from_df(df):
#        return df.apply(lambda x: Event(**x.squeeze()), axis=0)


