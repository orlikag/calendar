import unittest
import functions as f


class TestPrices(unittest.TestCase):

    def test_valid_price(self):
        cal = f.Main_Calendar("testDB.csv")
        start = f.time_format("7/8/2019", "20:00")
        end = f.time_format("7/8/2019", "23:30")
        title = "rosa"
        event_type = "pub"
        price = "a"
        new_event = f.Event(start=start, end=end, title=title, event_type=event_type, price=price)
        cal.set_event(new_event)
        new_event = cal.get_event(start=start, end=end, title=title)
        self.assertEqual(new_event.price, cal.calculate_average_price("pub"))
        self.assertFalse(new_event.input_price)

    def test_input_price(self):
        cal = f.Main_Calendar("testDB.csv")
        start = f.time_format("8/8/2019", "20:00")
        end = f.time_format("8/8/2019", "23:30")
        title = "rosa"
        event_type = "pub"
        new_event = f.Event(start=start, end=end, title=title, event_type=event_type)
        cal.set_event(new_event)
        new_event = cal.get_event(start=start, end=end, title=title)
        self.assertEqual(new_event.price, float(150))

    def test_sum_period(self):
        cal = f.Main_Calendar("testDB.csv")
        start = f.time_format("1/8/2019", "00:00")
        end = f.time_format("31/8/2019", "23:59")
        _, period_sum = cal.period(start, end)
        self.assertEqual(period_sum, float(170))


class TestDates(unittest.TestCase):

    def test_date_validation(self):
        start = f.time_format("9/8/2019", "10:00")
        end = f.time_format("8/8/2019", "11:00")
        check_time = f.date_validation(start, end)
        self.assertFalse(check_time)


if __name__ == '__main__':
    unittest.main()