import pandas as pd
import datetime
from calendar import monthrange
from prettytable import PrettyTable

timestamp_format = "%d/%m/%Y %H:%M"

def check_date(date):
    try:
        datetime.datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def check_time(time):
    try:
        datetime.datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False


def get_date(when):
    check = False
    while not check:
        date = input(f"{when} date: ")
        check = check_date(date)
        if not check:
            print("date should be in format: DD/MM/YYYY")
    return date


def get_time(when):
    check = False
    while not check:
        time = input(f"{when} time: ")
        check = check_time(time)
        if not check:
            print("time should be in format: HH:MM")
    return time


def time_format(date, time):
    day, month, year = date.split("/")
    hour, minute = time.split(":")
    date_time = pd.Timestamp(int(year), int(month), int(day), int(hour), int(minute))
    return date_time


class Event(object):

    def __init__(self, start, end, title, **kwargs):
        self.start = start
        self.end = end
        self.title = title
        self.event_type = None
        self.price = None
        self.invitees = None
        self.location = None
        self.repeat = None
        self.index = None
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.input_price = self.price is not None

    def __str__(self):
        event_str = f"Title: {self.title}\nType: {self.event_type}\nPrice: {self.price}\n" \
            f"Start: {self.start}\n" \
            f"End: {self.end}\nInvitees: {self.invitees}\n" \
            f"Location: {self.location}\nRepeat: {self.repeat}"
        return event_str

    def to_dict(self):
        event_dict = {'start':self.start, 'end':self.end, 'title':self.title, 'event_type':self.event_type,
                      'price':self.price, 'input_price': self.input_price, 'invitees':self.invitees, 'location':self.location, 'repeat':self.repeat}
        return event_dict

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self


class Main_Calendar(object):

    def __init__(self, file_name):
        self.DB = pd.read_csv(file_name, encoding='utf-8', parse_dates=['start', 'end'], dayfirst=True)

    def get_event(self, start, end, title):
        my_event = self.DB[(self.DB.start == start) & (self.DB.end == end) & (self.DB.title == title)]
        return Event(**my_event.squeeze())

    def __str__(self):
        return self.DB.__str__()

    def create_event(self,event):
        if self.duplication_check(event):
            exist_event = self.get_event(event.start, event.end, event.title)
            self.drop_event(exist_event)
        self.set_event(event)

    def set_event(self, event):
        event = self.check_price(event)
        self.DB = self.DB.append(pd.Series(data=event.to_dict()), ignore_index=True)

    def drop_event(self, event):
        event_index = self.DB[(self.DB.start == event.start) & (self.DB.end == event.end) & (self.DB.title == event.title)].index[0]
        self.DB = self.DB.drop(event_index)

    def update_event(self, start_origin, end_origin, title_origin, **kwargs):
        event = self.get_event(start_origin, end_origin, title_origin)
        self.drop_event(event)
        event = event.update(**kwargs)
        self.set_event(event)

    def save_calendar(self):
        self.DB.sort_values(['start', 'end'], inplace=True)
        self.DB.to_csv('demoDB1.csv', encoding='utf-8')

    def period(self, start, end):
        period_events = self.DB[(self.DB.start >= start) & (self.DB.start <= end)]
        return period_events, period_events["price"].sum()

    def get_day(self, start):
        end = start + datetime.timedelta(hours=23, minutes=59)
        return self.period(start, end)

    def get_month(self, month, year):
        start = time_format(f"1/{month}/{year}", "00:00")
        end = time_format(f"{monthrange(int(year),int(month))[1]}/{month}/{year}", "23:59")
        return self.period(start, end)

    def duplication_check(self, event):
        exist = self.DB[(self.DB.start == event.start) & (self.DB.end == event.end) & (self.DB.title == event.title)] is not None
        return exist

    def check_price(self,event):
        if not event.input_price:  # replace with event.update_price()
            event.update(price=self.calculate_average_price(event.event_type))
        return event

    def calculate_average_price(self, event_type):
        all_events = self.DB[(self.DB.event_type == event_type) & (self.DB.input_price)]
        return all_events["price"].mean()

    def print_day(self, day):
        if type(day) is not pd.Timestamp:
            day = time_format(day, "00:00")
        event_list, total_price = self.get_day(day)
        event_list = list(event_list.values)
        print(day.strftime("%A"), day.strftime("%d/%m/%Y"))
        print("===================")
        print(f"Total today: {total_price}")
        print("-------------------")
        for event in event_list:
            print(f"{event[0].strftime(timestamp_format)} - {event[1].strftime(timestamp_format)}    {event[2]}")
        print("")

    def print_week(self, day):
        given_day = time_format(day, "00:00")
        today = given_day - datetime.timedelta(days=int(given_day.strftime("%w")))
        for i in range(7):
            self.print_day(today)
            today += datetime.timedelta(days=1)

    @staticmethod
    def events_from_df(df):
        return df.apply(lambda x: Event(**x.squeeze()), axis=0)

