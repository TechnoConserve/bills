import os
import pytest
import calendar
from contextlib import contextmanager
from datetime import date
from random import randint

from peewee import SqliteDatabase

from db import categories, Housemate, IndividualBill, get_gas_total

example_totals = [2253, 342, 99, 10000]


@contextmanager
@pytest.fixture(autouse=True)
def initialize_db(tmpdir):
    db = SqliteDatabase(os.path.join(tmpdir, 'bills_test.db'))
    db.connect()
    db.create_tables([Housemate, IndividualBill])
    try:
        yield db
    finally:
        db.close()
        db.drop_tables([Housemate, IndividualBill])


@pytest.fixture()
def example_housemates():
    return (Housemate(name="Bob", email="bob@email.com"),
            Housemate(name="Jill", email="jill@comcast.net"),
            Housemate(name="Jimbo", email="notme@anonymous.net"),
            Housemate(name="Sally", email="prettyflowers@meadowwonderland.org"))


@pytest.fixture()
def random_bills(example_housemates):
    # Save housemates
    for housemate in example_housemates:
        housemate.save()

    # Create 30 random bills
    for i in range(30):
        random_year = randint(2019, 2050)
        random_month = randint(1, 12)
        # Subtract from last day of month so I can make sure there're
        # still days left in the month for the service end date
        random_day = randint(1, calendar.monthrange(random_year, random_month)[1] - 5)
        bill = IndividualBill(debtor=example_housemates[randint(0, len(example_housemates) - 1)],
                              service_start=date(year=random_year,
                                                 month=random_month,
                                                 day=random_day),
                              service_end=date(year=random_year,
                                               month=random_month,
                                               day=random_day + 5),
                              category=categories[randint(0, len(categories) - 1)][0],
                              total=randint(1, 10000),
                              paid=randint(0, 1))
        bill.save()


@pytest.fixture()
def example_gas_bills(example_housemates):
    # Save the housemates so we can use them
    example_housemates[0].save()
    example_housemates[1].save()
    example_housemates[2].save()

    bill1 = IndividualBill(debtor=example_housemates[0],
                           service_start=date(year=2019,
                                              month=1,
                                              day=1),
                           service_end=date(year=2019,
                                            month=2,
                                            day=1),
                           category=categories[0][0],
                           total=example_totals[0],
                           paid=False)
    bill2 = IndividualBill(debtor=example_housemates[1],
                           service_start=date(year=2019,
                                              month=1,
                                              day=1),
                           service_end=date(year=2019,
                                            month=2,
                                            day=1),
                           category=categories[0][0],
                           total=example_totals[1],
                           paid=False)
    bill3 = IndividualBill(debtor=example_housemates[2],
                           service_start=date(year=2019,
                                              month=1,
                                              day=1),
                           service_end=date(year=2019,
                                            month=2,
                                            day=1),
                           category=categories[0][0],
                           total=example_totals[2],
                           paid=False)
    bill1.save()
    bill2.save()
    bill3.save()


def test_gas_total(example_gas_bills):
    correct_total = example_totals[0] + example_totals[1] + example_totals[2]
    test_total = get_gas_total()
    assert correct_total == test_total


def test_housemate_creation(random_bills):
    assert IndividualBill.select().count() == 30
