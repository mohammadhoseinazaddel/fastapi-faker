import jdatetime


class JDateNavigator:
    def __init__(self, jalali_date: jdatetime.datetime):
        self.date = jalali_date
        self.year = jalali_date.year
        self.month = jalali_date.month
        self.day = jalali_date.day

    def next_month(self, first_day_of_next_month=False):
        self.day = 1
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self._recalculate_time()

    def _recalculate_time(self):
        self.date = self.date.replace(
            year=self.year,
            month=self.month,
            day=self.day,
        )

    def replace(self, year=None, month=None, day=None):
        if year:
            self.date = self.date.replace(year=year)
        if month:
            self.date = self.date.replace(month=month)
        if day:
            self.date = self.date.replace(day=day)

    def get_date_in_utc(self):
        return jdatetime.date.togregorian(self.date)

    def get_date_in_jalali(self):
        return self.date


def get_due_date(fixed_day=5):
    today = JDateNavigator(jalali_date=jdatetime.datetime.now())

    if today.day == fixed_day:
        return today.get_date_in_utc()
    if today.day > fixed_day:
        return today.get_date_in_utc()
    if today.day < fixed_day:
        return today.get_date_in_utc()

