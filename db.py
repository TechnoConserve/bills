"""Define models and functions for storage in a database."""
from peewee import *

db = SqliteDatabase('bills.db')
categories = [("gas", "Gas"), ("internet", "Internet"), ("power", "Power"), ("water", "Water")]


class BaseModel(Model):
    class Meta:
        database = db


class HouseMate(BaseModel):
    name = CharField(unique=True)
    email = CharField(unique=True)

    def amount_owed(self):
        pass


class IndividualBill(BaseModel):
    debtor = ForeignKeyField(HouseMate, backref="bills")

    # Service Period
    service_start = DateField(null=False)
    service_end = DateField(null=False)

    category = CharField(choices=categories, null=False, unique=True)

    # Total cost per individual using fixed-point representation
    total = IntegerField(null=False)

    paid = BooleanField(default=False)
