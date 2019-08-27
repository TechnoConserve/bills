import os
import pytest
import calendar
from contextlib import contextmanager
from datetime import date
import random
from random import randint

from peewee import SqliteDatabase

from db import categories, Housemate, IndividualBill, get_gas_total, get_internet_total, get_power_total, \
    get_water_total, get_housemates, get_total_owed, get_individual_bills, get_individual_unpaid_bills

MODELS = [Housemate, IndividualBill]
example_totals = [2253, 342, 99, 10000]


class DB:
    def __init__(self, tmpdir):
        self.db = SqliteDatabase(os.path.join(tmpdir, 'bills_test.db'))
        self.db.bind(MODELS)
        self.db.connect()
        self.db.create_tables(MODELS)
        self.db.close()

    def connect(self):
        self.db.connect()

    def close(self):
        self.db.close()

    def drop_tables(self):
        self.db.drop_tables(MODELS)


@pytest.fixture()
def db(tmpdir):
    return DB(tmpdir)


class TestDB:
    @contextmanager
    @pytest.fixture(autouse=True)
    def initialize_db(self, tmpdir, db):
        try:
            db.connect()
            yield
        finally:
            db.close()
            db.drop_tables()

    @pytest.fixture()
    def example_housemates(self):
        return (Housemate(name="Bob", email="bob@email.com"),
                Housemate(name="Jill", email="jill@comcast.net"),
                Housemate(name="Jimbo", email="notme@anonymous.net"),
                Housemate(name="Sally", email="prettyflowers@meadowwonderland.org"))

    @pytest.fixture()
    def random_bills(self, example_housemates, db):
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
            bill = IndividualBill(debtor=random.choice(example_housemates),
                                  service_start=date(year=random_year,
                                                     month=random_month,
                                                     day=random_day),
                                  service_end=date(year=random_year,
                                                   month=random_month,
                                                   day=random_day + 5),
                                  category=random.choice(categories)[0],
                                  total=randint(1, 10000),
                                  paid=randint(0, 1))
            bill.save()

    @pytest.fixture()
    def example_gas_bills(self, example_housemates, db):
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

    @pytest.fixture()
    def example_internet_bills(self, example_housemates, db):
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
                               category=categories[1][0],
                               total=example_totals[0],
                               paid=False)
        bill2 = IndividualBill(debtor=example_housemates[1],
                               service_start=date(year=2019,
                                                  month=1,
                                                  day=1),
                               service_end=date(year=2019,
                                                month=2,
                                                day=1),
                               category=categories[1][0],
                               total=example_totals[1],
                               paid=False)
        bill3 = IndividualBill(debtor=example_housemates[2],
                               service_start=date(year=2019,
                                                  month=1,
                                                  day=1),
                               service_end=date(year=2019,
                                                month=2,
                                                day=1),
                               category=categories[1][0],
                               total=example_totals[2],
                               paid=False)
        bill1.save()
        bill2.save()
        bill3.save()

    @pytest.fixture()
    def example_power_bills(self, example_housemates, db):
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
                               category=categories[2][0],
                               total=example_totals[0],
                               paid=False)
        bill2 = IndividualBill(debtor=example_housemates[1],
                               service_start=date(year=2019,
                                                  month=1,
                                                  day=1),
                               service_end=date(year=2019,
                                                month=2,
                                                day=1),
                               category=categories[2][0],
                               total=example_totals[1],
                               paid=False)
        bill3 = IndividualBill(debtor=example_housemates[2],
                               service_start=date(year=2019,
                                                  month=1,
                                                  day=1),
                               service_end=date(year=2019,
                                                month=2,
                                                day=1),
                               category=categories[2][0],
                               total=example_totals[2],
                               paid=False)
        bill1.save()
        bill2.save()
        bill3.save()

    @pytest.fixture()
    def example_water_bills(self, example_housemates, db):
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
                               category=categories[3][0],
                               total=example_totals[0],
                               paid=False)
        bill2 = IndividualBill(debtor=example_housemates[1],
                               service_start=date(year=2019,
                                                  month=1,
                                                  day=1),
                               service_end=date(year=2019,
                                                month=2,
                                                day=1),
                               category=categories[3][0],
                               total=example_totals[1],
                               paid=False)
        bill3 = IndividualBill(debtor=example_housemates[2],
                               service_start=date(year=2019,
                                                  month=1,
                                                  day=1),
                               service_end=date(year=2019,
                                                month=2,
                                                day=1),
                               category=categories[3][0],
                               total=example_totals[2],
                               paid=False)
        bill1.save()
        bill2.save()
        bill3.save()

    def test_gas_total(self, example_gas_bills):
        correct_total = example_totals[0] + example_totals[1] + example_totals[2]
        test_total = get_gas_total()
        assert test_total == correct_total

    def test_internet_total(self, example_internet_bills):
        correct_total = example_totals[0] + example_totals[1] + example_totals[2]
        test_total = get_internet_total()
        assert test_total is not None
        assert test_total == correct_total

    def test_power_total(self, example_power_bills):
        correct_total = example_totals[0] + example_totals[1] + example_totals[2]
        test_total = get_power_total()
        assert test_total is not None
        assert test_total == correct_total

    def test_water_total(self, example_water_bills):
        correct_total = example_totals[0] + example_totals[1] + example_totals[2]
        test_total = get_water_total()
        assert test_total is not None
        assert test_total == correct_total

    def test_housemate_creation(self, random_bills):
        assert IndividualBill.select().count() == 30

    def test_get_housemates(self, example_housemates):
        housemates = get_housemates()
        assert len(housemates) == 0
        example_housemates[0].save()
        housemates = get_housemates()
        assert len(housemates) == 1
        example_housemates[1].save()
        example_housemates[2].save()
        housemates = get_housemates()
        assert len(housemates) == 3

    def test_total_owed(self, example_gas_bills, example_internet_bills, example_power_bills,
                        example_water_bills, example_housemates):
        correct_total = example_totals[0] * 4
        test_total = get_total_owed(example_housemates[0])
        assert test_total == correct_total

    def test_get_individual_bills(self, example_housemates, example_water_bills, example_power_bills,
                                  example_internet_bills, example_gas_bills):
        assert get_individual_bills(example_housemates[0]).count() == 4

    def test_get_individual_unpaid_bills(self, example_housemates, example_gas_bills, example_internet_bills,
                                         example_power_bills, example_water_bills):
        assert get_individual_unpaid_bills(example_housemates[0]).count() == 4

        # Add a paid bill
        paid_bill = IndividualBill(debtor=example_housemates[0],
                                   service_start=date(year=2019,
                                                      month=1,
                                                      day=1),
                                   service_end=date(year=2019,
                                                    month=2,
                                                    day=1),
                                   category=categories[3][0],
                                   total=example_totals[0],
                                   paid=True)
        paid_bill.save()

        # Number of unpaid bills should not have changed
        assert get_individual_unpaid_bills(example_housemates[0]).count() == 4

        # Add another unpaid bill
        unpaid_bill = IndividualBill(debtor=example_housemates[0],
                                     service_start=date(year=2019,
                                                        month=1,
                                                        day=1),
                                     service_end=date(year=2019,
                                                      month=2,
                                                      day=1),
                                     category=categories[3][0],
                                     total=example_totals[0],
                                     paid=False)
        unpaid_bill.save()

        # Now there should be 5 unpaid bills
        assert get_individual_unpaid_bills(example_housemates[0]).count() == 5
