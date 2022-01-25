'''has all coding for time & date related queries for Py-Calendar application'''

import datetime as dt
from typing import Union


##############
# TIME LOGIC #
##############

class DateCalc:
    """Defines all that required for date calculation"""

    def __init__(self) -> None:
        """A Basic Date Calculator"""

    @staticmethod
    def day_calculator(start_date, end_date) -> int:
        '''Gives number of days between entered dates'''

        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

        if end_date < start_date:
            raise ValueError("End date was found to be less than start date")
        else:
            return (end_date - start_date).days

    @staticmethod
    def second_calculator(start_date, end_date) -> float:
        '''Gives number of seconds between entered date'''

        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

        return (start_date - end_date).total_seconds()

    @staticmethod
    def date_increment(date, increment: int, increment_unit: str) -> dt.date:
        '''Gives date after given number of days'''

        if increment_unit == 'week(s)':
            increment *= 7
        elif increment_unit == 'month(s)':
            increment *= 30
        elif increment_unit == 'year(s)':
            increment *= 365

        date = dt.datetime.strptime(date, "%Y-%m-%d")
        date += dt.timedelta(days=increment)
        return date


class TimeConvert:
    '''Class for converting any amount of seconds to days, weeks, and years'''

    def __init__(self, integer: int, unit: str, out_unit: str) -> Union[int, float]:
        '''Requires seconds to initiate and converts it to other units of time'''

        self.num = integer
        self.in_unit = unit
        self.out_unit = out_unit

        self.second = self._to_sec()

    def _to_sec(self) -> int:
        '''converts given data to seconds'''

        # necessary dict having unit: multiplier -> sec
        conversion: dict = {
            'min': 60,
            'hour': 60 * 60,
            'day(s)': 24 * 60 * 60,
            'week(s)': 7 * 24 * 60 * 60,
            'year(s)': 365 * 24 * 60 * 60,
        }
        return self.num * conversion[self.in_unit]

    def _to_min(self) -> int:
        '''Returns sec to mins'''
        return self.second / 60

    def _to_hour(self) -> int:
        '''Returns sec to hours'''
        return self._to_min() / 60

    def _to_days(self) -> int:
        '''Returns number of days'''
        return round(self._to_hour() / 24, 3)

    def _to_weeks(self) -> int:
        '''Returns number of weeks in int form'''
        return round(self._to_days() / 7, 3)

    def _to_year(self) -> int:
        '''Returns number of years in int form'''
        return round(self._to_days() / 365, 3)

    def output(self):
        conversion_func = {
            'sec': self._to_sec,
            'min': self._to_min,
            'hour': self._to_hour,
            'day(s)': self._to_days,
            'week(s)': self._to_weeks,
            'year(s)': self._to_year
        }
        return conversion_func[self.out_unit]()


class TimeCalc():
    '''A Basic Time calculator'''

    def __init__(self) -> None:
        '''A basic Time calculator'''

    @staticmethod
    def str_to_seconds(timestr: str) -> int:
        '''Converts entered time to seconds with 00:00:00 as 0 sec for reference, format=[%i%i:%i%i:%i%i]'''

        multipliers = [3600, 60, 1]
        return sum([a * b for a, b in zip(multipliers, map(int, timestr.split(':')))])

    def time_gap(self, start_time: str, end_time: str) -> Union[int, ValueError]:
        '''Returns seconds difference between entered times'''

        if (dt.time.fromisoformat(start_time) > dt.time.fromisoformat(end_time)):
            raise ValueError("Start time can't be bigger than end time")
        else:
            return self.str_to_seconds(end_time) - self.str_to_seconds(start_time)

    @staticmethod
    def time_increment(time: str, increment: int, increment_unit: str) -> str:
        '''Increments time by given seconds and returns formed string'''

        # changing value such that it will always give corresponding seconds
        if increment_unit == 'hrs':
            increment *= 3600
        elif increment_unit == 'min':
            increment *= 60

        # removing 0 from left side so no problem occurs when converting to int
        time: list = time.split(':')
        time = [int(time[i].lstrip('0')) for i in range(3)]
        hours, minutes, seconds = time

        # converting above data to timedelta to do the actual increment
        total_seconds = dt.timedelta(
            hours=hours, minutes=minutes, seconds=seconds) + dt.timedelta(seconds=increment)

        # returns string in format of "%i%i:%i%i:%i%i" if it passes a 24 hours then %i Days, same time format
        return str(total_seconds)
