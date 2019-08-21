"""Define models and functions for storage in a database."""
from peewee import *

db = SqliteDatabase('bills.db')
categories = [("gas", "Gas"), ("internet", "Internet"), ("power", "Power"), ("water", "Water")]


class BaseModel(Model):
    class Meta:
        database = db


class Housemate(BaseModel):
    name = CharField(unique=True)
    email = CharField(unique=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def amount_owed(self):
        pass


class IndividualBill(BaseModel):
    debtor = ForeignKeyField(Housemate, backref="bills")

    # Service Period
    service_start = DateField(null=False)
    service_end = DateField(null=False)

    category = CharField(choices=categories, null=False)

    # Total cost per individual using fixed-point representation
    total = IntegerField(null=False)

    paid = BooleanField(default=False)


def create_tables():
    with db:
        db.create_tables([Housemate, IndividualBill])


def get_housemates():
    return Housemate.select()


def get_gas_total():
    return IndividualBill.select(fn.SUM(IndividualBill.total))\
        .where(IndividualBill.category == categories[0][0]).scalar()


def get_internet_total():
    return IndividualBill.select(fn.SUM(IndividualBill.total))\
        .where(IndividualBill.category == categories[1][0]).scalar()


def get_power_total():
    return IndividualBill.select(fn.SUM(IndividualBill.total))\
        .where(IndividualBill.category == categories[2][0]).scalar()


def get_water_total():
    return IndividualBill.select(fn.SUM(IndividualBill.total))\
        .where(IndividualBill.category == categories[3][0]).scalar()


def get_total_owed(housemate):
    return IndividualBill.select(fn.SUM(IndividualBill.total))\
        .where(IndividualBill.paid == False, IndividualBill.debtor == housemate).scalar()
