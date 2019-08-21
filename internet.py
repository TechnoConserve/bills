import calendar
from datetime import datetime

from db import categories
from models import Bill


def get_internet_bill(year, month):
    """
    Create a Bill object for the internet bill using
    the given month to determine the service period.
    :param year: Integer representing the year of
    service covered by the bill.
    :param month: Integer representing the month
    of service covered by the bill.
    :return: Bill object for the internet.
    """
    last_day_of_month = calendar.monthrange(year, month)[1]
    internet_bill = Bill(start_date=datetime(year=year, month=month, day=1),
                         end_date=datetime(year=year, month=month, day=last_day_of_month),
                         category=categories[1][0],
                         total=50.00)

    return internet_bill
